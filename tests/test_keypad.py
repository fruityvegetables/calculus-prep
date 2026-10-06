from src.keypad import apply_key


def test_sqrt_wraps_a_trailing_number():
    assert apply_key("72", "sqrt") == ("sqrt(72)", False)
    assert apply_key("6*2", "sqrt") == ("6*sqrt(2)", False)
    assert apply_key("6 * 2", "sqrt") == ("6 * sqrt(2)", False)


def test_sqrt_keeps_a_unary_minus_and_drops_a_binary_one():
    assert apply_key("-3", "sqrt") == ("sqrt(-3)", False)
    assert apply_key("2*-4", "sqrt") == ("2*sqrt(-4)", False)
    assert apply_key("6-2", "sqrt") == ("6-sqrt(2)", False)
    assert apply_key("-(x+1)", "sqrt") == ("sqrt(-(x+1))", False)
    assert apply_key("6-(x+1)", "sqrt") == ("6-sqrt((x+1))", False)


def test_sqrt_wraps_a_variable_or_parenthesized_group():
    assert apply_key("x", "sqrt") == ("sqrt(x)", False)
    assert apply_key("(x+1)", "sqrt") == ("sqrt((x+1))", False)
    assert apply_key("(x+(1))", "sqrt") == ("sqrt((x+(1)))", False)


def test_empty_function_then_digits_land_inside():
    edit = apply_key("", "sqrt")
    assert edit == ("sqrt()", True)
    edit = apply_key(edit.text, "7", fill=edit.fill)
    edit = apply_key(edit.text, "2", fill=edit.fill)
    assert edit == ("sqrt(72)", True)
    edit = apply_key("6*", "sqrt")
    assert edit == ("6*sqrt()", True)
    edit = apply_key(edit.text, ".", fill=edit.fill)
    edit = apply_key(edit.text, "5", fill=edit.fill)
    assert edit == ("6*sqrt(.5)", True)


def test_pi_and_x_land_inside_an_open_function():
    edit = apply_key("sqrt()", "pi", fill=True)
    assert edit == ("sqrt(pi)", True)
    edit = apply_key("sin()", "x", fill=True)
    assert edit == ("sin(x)", True)


def test_operator_or_closing_paren_leaves_the_function():
    assert apply_key("sqrt(72)", "*", fill=True) == ("sqrt(72)*", False)
    assert apply_key("sqrt(72)", ")", fill=True) == ("sqrt(72)", False)
    assert apply_key("sqrt(72", ")") == ("sqrt(72)", False)


def test_backspace_removes_the_character_inside_while_filling():
    assert apply_key("sqrt(72)", "backspace", fill=True) == ("sqrt(7)", True)
    assert apply_key("sqrt(7)", "backspace", fill=True) == ("sqrt()", True)
    assert apply_key("sqrt()", "backspace", fill=True) == ("sqrt(", False)
    assert apply_key("sqrt(72)", "backspace", fill=False) == ("sqrt(72", False)
    assert apply_key("", "backspace") == ("", False)


def test_plain_keys_and_other_functions():
    assert apply_key("8", "/") == ("8/", False)
    assert apply_key("2", "*") == ("2*", False)
    assert apply_key("", "pi") == ("pi", False)
    assert apply_key("0", "sin") == ("sin(0)", False)
    assert apply_key("pi/2", "cos") == ("pi/cos(2)", False)
    assert apply_key("x", "tan") == ("tan(x)", False)
