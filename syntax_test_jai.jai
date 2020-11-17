// SYNTAX TEST "Packages/JaiTools/Jai.sublime-syntax"

  #import "Basic";
//^^^^^^^ keyword.control.import.jai
//        ^^^^^^^ string.quoted.double.jai
//               ^ punctuation.terminator.jai

  my_var := 42;
//^^^^^^ variable.other.jai
//       ^^ keyword.operator.assignment.jai
//          ^^ constant.numeric.integer.decimal.jai
//            ^ punctuation.terminator.jai
//^^^^^^^^^^^^^ meta.variable.jai

  MY_VAR := "my string";
//^^^^^^ variable.other.jai
//       ^^ keyword.operator.assignment.jai
//          ^^^^^^^^^^^ string.quoted.double.jai
//                     ^ punctuation.terminator.jai
//^^^^^^^^^^^^^^^^^^^^^^ meta.variable.jai

  my_var_123 := my_func();
//^^^^^^^^^^ variable.other.jai
//           ^^ keyword.operator.assignment.jai
//              ^^^^^^^ variable.function.jai
//              ^^^^^^^^^ meta.function-call.jai
//                       ^ punctuation.terminator.jai
//^^^^^^^^^^^^^^^^^^^^^^^^ meta.variable.jai

  commented_var_0 := /**/ 42 /**/ ;
//^^^^^^^^^^^^^^^ variable.other.jai
//                ^^ keyword.operator.assignment.jai
//                   ^^^^ comment.block.jai
//                        ^^ constant.numeric.integer.decimal.jai
//                           ^^^^ comment.block.jai
//                                ^ punctuation.terminator.jai
//^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.variable.jai
  
  commented_var_0 : int = 42;
//^^^^^^^^^^^^^^^ variable.other.jai
//                ^ keyword.operator.assignment.jai
//                  ^^^ storage.type.jai
//                      ^ keyword.operator.assignment.jai
//                        ^^ constant.numeric.integer.decimal.jai
//                          ^ punctuation.terminator.jai
//^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.variable.jai

  my_negative_float := -2_3_5.0_1_3_5_3_1;
//                     ^ keyword.operator.arithmetic.jai
//                      ^^^^^^^^^^^^^^^^^ constant.numeric.float.decimal.jai

my_parenthesis_var := (my_negative_float + 3.0) * commented_var_1;

  my_array : [4] int;
//^^^^^^^^ variable.other.jai
//         ^ keyword.operator.assignment.jai
//           ^ punctuation.section.brackets.begin.jai
//            ^ constant.numeric.integer.decimal.jai
//             ^ punctuation.section.brackets.end.jai
//               ^^^ storage.type.jai
//                  ^ punctuation.terminator.jai
//^^^^^^^^^^^^^^^^^^^ meta.variable.jai

  my_array : [my_var] My_Type;
//^^^^^^^^ variable.other.jai
//         ^ keyword.operator.assignment.jai
//           ^ punctuation.section.brackets.begin.jai
//            ^^^^^^ variable.other.jai
//                  ^ punctuation.section.brackets.end.jai
//                    ^^^^^^^ storage.type.jai
//                           ^ punctuation.terminator.jai
//^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.variable.jai

  my_func_0 :: () {
//^^^^^^^^^ entity.name.function.jai
//          ^^ keyword.operator.assignment.jai
//             ^ punctuation.section.parameters.begin.jai
//              ^ punctuation.section.parameters.end.jai
//                ^ meta.block.jai
//^^^^^^^^^^^^^^^ meta.function.jai
  }
//^ meta.block.jai

  my_func_1 :: (my_param: int) {
//^^^^^^^^^ entity.name.function.jai
//          ^^ keyword.operator.assignment.jai
//             ^ punctuation.section.parameters.begin.jai
//              ^^^^^^^^ variable.parameter.jai
//                      ^ punctuation.separator.jai
//                        ^^^ storage.type.jai
//                           ^ punctuation.section.parameters.end.jai
//                             ^ meta.block.jai
//^^^^^^^^^^^^^ meta.function.jai
  }
//^ meta.block.jai

  my_func_2 :: (my_param_0: My_Type, my_param_1: [] float) {
//^^^^^^^^^ entity.name.function.jai
//          ^^ keyword.operator.assignment.jai
//             ^ punctuation.section.parameters.begin.jai
//              ^^^^^^^^^^ variable.parameter.jai
//                        ^ punctuation.separator.jai
//                          ^^^^^^^ storage.type.jai
//                                 ^ punctuation.separator.jai
//                                   ^^^^^^^^^^ variable.parameter.jai
//                                             ^ punctuation.separator.jai
//                                               ^ punctuation.section.brackets.begin.jai
//                                                ^ punctuation.section.brackets.end.jai
//                                                  ^^^^^ storage.type.jai
//                                                       ^ punctuation.section.parameters.end.jai
//                                                         ^ meta.block.jai
//^^^^^^^^^^^^^ meta.function.jai
  }
//^ meta.block.jai

  my_func_3 :: (my_param_0: My_Type, my_param_1: [] float) -> string {
//^^^^^^^^^ entity.name.function.jai
//          ^^ keyword.operator.assignment.jai
//             ^ punctuation.section.parameters.begin.jai
//              ^^^^^^^^^^ variable.parameter.jai
//                        ^ punctuation.separator.jai
//                          ^^^^^^^ storage.type.jai
//                                 ^ punctuation.separator.jai
//                                   ^^^^^^^^^^ variable.parameter.jai
//                                             ^ punctuation.separator.jai
//                                               ^ punctuation.section.brackets.begin.jai
//                                                ^ punctuation.section.brackets.end.jai
//                                                  ^^^^^ storage.type.jai
//                                                       ^ punctuation.section.parameters.end.jai
//                                                         ^^ keyword.other.jai
//                                                            ^^^^^^ storage.type.jai
//                                                                   ^ meta.block.jai
//^^^^^^^^^^^^^ meta.function.jai
  }
//^ meta.block.jai

multi_line_func_0 :: (
	my_param_0: My_Type,
	my_param_1: [] float) -> string
{
	
}

multi_line_func_1 :: (my_param_0: My_Type,
	my_param_1: [] float
	) -> string
{
	
}

multi_line_func_1(f, 4);

for element: array {
	
}

for element: array
{
	
}

  My_Struct :: struct {
//^^^^^^^^^ entity.name.struct.jai
todo: struct stuff.
}

main :: () {
  local_var_0 := 42.42;
  print("A is of type %, value %.\n", type_of(local_var), local_var);
//^^^^^ meta.function-call.jai
//      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ string.quoted.double.jai
//                    ^ constant.other.placeholder.jai
//                               ^^ constant.character.escape.jai
//                                    ^^^^^^^ meta.function-call.jai
//                                                                  ^ punctuation.terminator.jai

// handle casts as a special case, so we can color the type that is being cast to. i.e. match 'cast' and 'cast,no_check', not the syntax for a function call.
  cast(My_Struct) 4;
//^^^^ meta.function-call.jai
//     ^^^^^^^^^ storage.type.jai
//                ^ constant.numeric.integer.decimal.jai

  cast,no_check(int) my_negative_float;
//^^^^^^^^^^^^^ meta.function-call.jai
//              ^^^ storage.type.jai
//                   ^ variable.other.jai
} // end of main()

  for index: 0..7 {
//^^^ keyword.control.jai
//    ^^^^^ variable.other.jai
//         ^ punctuation.separator.jai
//           ^ constant.numeric.integer.decimal.jai
//            ^^ keyword.other.jai
//              ^ constant.numeric.integer.decimal.jai
}












