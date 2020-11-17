// SYNTAX TEST "Packages/JaiTools/Jai.sublime-syntax"

  my_var := 42;
//^^^^^^ entity.name.variable.jai
//       ^^ keyword.operator.assignment.jai
//          ^^ constant.numeric.integer.decimal.jai
//^^^^^^^^^^^^^ meta.variable.jai

  MY_VAR := "my string";
//^^^^^^ entity.name.variable.jai
//       ^^ keyword.operator.assignment.jai
//          ^^^^^^^^^^^ string.quoted.double.jai
//^^^^^^^^^^^^^^^^^^^^^^ meta.variable.jai

  my_var_123 := my_func();
//^^^^^^^^^^ entity.name.variable.jai
//           ^^ keyword.operator.assignment.jai
//              ^^^^^^^ variable.function.jai
//              ^^^^^^^^^ meta.function-call.jai
//^^^^^^^^^^^^^^^^^^^^^^^^ meta.variable.jai

  my_array : [4] int;
//^^^^^^ entity.name.variable.jai
//         ^ keyword.operator.assignment.jai
//           ^ punctuation.section.brackets.begin.jai
//            ^ constant.numeric.integer.decimal.jai
//             ^ punctuation.section.brackets.end.jai
//               ^ storage.type.jai
//^^^^^^^^^^^^^^^^^^^ meta.variable.jai

  my_array : [my_var] My_Type;
//^^^^^^^^ entity.name.variable.jai
//         ^ keyword.operator.assignment.jai
//           ^ punctuation.section.brackets.begin.jai
//            ^^^^^^ variable.other.jai
//                  ^ punctuation.section.brackets.end.jai
//                    ^^^^^^^ storage.type.jai
//^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.variable.jai

  my_func_0 :: () {
//^^^^^^^^^ entity.name.function.jai
//          ^^ keyword.operator.assignment.jai
//             ^ punctuation.section.brackets.begin.jai
//             ^^ meta.function.parameters.jai
//             ^ punctuation.section.parameters.begin.jai
//              ^ punctuation.section.parameters.end.jai
//                ^ meta.block.jai punctuation.section.block.begin.jai
//^^^^^^^^^^^^^^^ meta.function.jai
  }
//^ meta.block.jai punctuation.section.block.end.jai

  my_func_1 :: (my_param: int) {
//^^^^^^^^^ entity.name.function.jai
//          ^^ keyword.operator.assignment.jai
//             ^ punctuation.section.brackets.begin.jai
//             ^ punctuation.section.parameters.begin.jai
//              ^^^^^^^^ variable.parameter.jai
//                      ^ punctuation.separator.jai
//                        ^^^ storage.type.jai
//                           ^ punctuation.section.parameters.end.jai
//             ^^^^^^^^^^^^^^^ meta.function.parameters.jai
//                             ^ meta.block.jai punctuation.section.block.begin.jai
//^^^^^^^^^^^^^ meta.function.jai
}
//^ meta.block.jai punctuation.section.block.end.jai

  my_func_2 :: (my_param_0: My_Type, my_param_1: [] float) {
//^^^^^^^^^ entity.name.function.jai
//          ^^ keyword.operator.assignment.jai
//             ^ punctuation.section.brackets.begin.jai
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
//             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.function.parameters.jai
//                                                         ^ meta.block.jai punctuation.section.block.begin.jai
//^^^^^^^^^^^^^ meta.function.jai
  }
//^ meta.block.jai punctuation.section.block.end.jai

  my_func_3 :: (my_param_0: My_Type, my_param_1: [] float) -> string {
//^^^^^^^^^ entity.name.function.jai
//          ^^ keyword.operator.assignment.jai
//             ^ punctuation.section.brackets.begin.jai
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
//                                                                   ^ meta.block.jai punctuation.section.block.begin.jai
//^^^^^^^^^^^^^ meta.function.jai
//             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.function.parameters.jai
//                                                            ^^^^^^ meta.function.return-type.jai
  }
//^ meta.block.jai punctuation.section.block.end.jai

cast(My_Type) 4;
cast,no_check(My_Type) 4;

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














