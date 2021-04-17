// SYNTAX TEST "Packages/JaiToolsDev/Jai.sublime-syntax"

  #import "Basic";
//^^^^^^^ keyword.control.import.jai
//        ^^^^^^^ string.quoted.double.jai
//               ^ punctuation.terminator.jai

THE_STRING :: #string DONE
This is a herestring.
DONE



  my_var := 42;
//^^^^^^ variable.other.jai
//       ^^ keyword.operator.assignment.jai
//          ^^ constant.numeric.jai
//            ^ punctuation.terminator.jai
//^^^^^^^^^^^^^ meta.variable.jai

  MY_VAR := "my string";
//^^^^^^ variable.other.jai
//       ^^ keyword.operator.assignment.jai
//          ^^^^^^^^^^^ string.quoted.double.jai
//                     ^ punctuation.terminator.jai
//^^^^^^^^^^^^^^^^^^^^^^ meta.variable.jai

  commented_var_0 := /**/ 42 /**/ ;
//^^^^^^^^^^^^^^^ variable.other.jai
//                ^^ keyword.operator.assignment.jai
//                   ^^^^ comment.block.jai
//                        ^^ constant.numeric.jai
//                           ^^^^ comment.block.jai
//                                ^ punctuation.terminator.jai
//^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.variable.jai
  
  commented_var_1 : int = 42;
//^^^^^^^^^^^^^^^ variable.other.jai
//                ^ keyword.operator.assignment.jai
//                  ^^^ storage.type.jai
//                      ^ keyword.operator.assignment.jai
//                        ^^ constant.numeric.jai
//                          ^ punctuation.terminator.jai
//^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.variable.jai

  my_negative_float := -2_3_5.0_1_3_5_3_1;
//                     ^ keyword.operator.arithmetic.jai
//                      ^^^^^^^^^^^^^^^^^ constant.numeric.jai

  my_array : [4] int;
//^^^^^^^^ variable.other.jai
//         ^ keyword.operator.assignment.jai
//           ^ punctuation.section.brackets.begin.jai
//            ^ constant.numeric.jai
//             ^ punctuation.section.brackets.end.jai
//               ^^^ storage.type.jai
//                  ^ punctuation.terminator.jai
//^^^^^^^^^^^^^^^^^^^ meta.variable.jai

  my_array2 : [my_var] Abcdefe;
//^^^^^^^^^ variable.other.jai
//          ^ keyword.operator.assignment.jai
//            ^ punctuation.section.brackets.begin.jai
//                   ^ punctuation.section.brackets.end.jai
//                     ^^^^^^^ storage.type.jai
//                            ^ punctuation.terminator.jai
//^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.variable.jai

  pointer_array : *[] int;
//^^^^^^^^^^^^^ variable.other.jai
//              ^ keyword.operator.assignment.jai
//                ^ keyword.operator.jai
//                 ^ punctuation.section.brackets.begin.jai
//                  ^ punctuation.section.brackets.end.jai
//                    ^^^ storage.type.jai
//                       ^ punctuation.terminator.jai
//^^^^^^^^^^^^^^^^^^^^^^^^ meta.variable.jai

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
//                      ^ keyword.operator.assignment.jai
//                        ^^^ storage.type.jai
//                           ^ punctuation.section.parameters.end.jai
//                             ^ meta.block.jai
//^^^^^^^^^^^^^ meta.function.jai
  }
//^ meta.block.jai

  my_func_2 :: (my_param_0: Abcdefe, my_param_1: [] float) {
//^^^^^^^^^ entity.name.function.jai
//          ^^ keyword.operator.assignment.jai
//             ^ punctuation.section.parameters.begin.jai
//              ^^^^^^^^^^ variable.parameter.jai
//                        ^ keyword.operator.assignment.jai
//                          ^^^^^^^ storage.type.jai
//                                 ^ punctuation.separator.jai
//                                   ^^^^^^^^^^ variable.parameter.jai
//                                             ^ keyword.operator.assignment.jai
//                                               ^ punctuation.section.brackets.begin.jai
//                                                ^ punctuation.section.brackets.end.jai
//                                                  ^^^^^ storage.type.jai
//                                                       ^ punctuation.section.parameters.end.jai
//                                                         ^ meta.block.jai
//^^^^^^^^^^^^^ meta.function.jai
  }
//^ meta.block.jai

  named_returns :: () -> return_0: string, return_1: int {
//^^^^^^^^^^^^^ entity.name.function.jai
//              ^^ keyword.operator.assignment.jai
//                 ^ punctuation.section.parameters.begin.jai
//                  ^ punctuation.section.parameters.end.jai
//                    ^^ keyword.other.jai
//                       ^^^^^^^^ variable.other.jai
//                               ^ keyword.operator.assignment.jai
//                                 ^^^^^^ storage.type.jai
//                                                       ^ meta.block.jai
//^^^^^^^^^^^^^^^^^ meta.function.jai
    return "ewf", 354;
  }
//^ meta.block.jai

  my_func_3 :: (my_param_0: Abcdefe, my_param_1: [] float) -> string {
//^^^^^^^^^ entity.name.function.jai
//          ^^ keyword.operator.assignment.jai
//             ^ punctuation.section.parameters.begin.jai
//              ^^^^^^^^^^ variable.parameter.jai
//                        ^ keyword.operator.assignment.jai
//                          ^^^^^^^ storage.type.jai
//                                 ^ punctuation.separator.jai
//                                   ^^^^^^^^^^ variable.parameter.jai
//                                             ^ keyword.operator.assignment.jai
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

to_c_string :: (s: string) -> *u8 {
    result := cast(*u8) alloc(s.count + 1);
    memcpy(result, s.data, s.count);
    result[s.count] = 0;

    return result;
}

  my_func :: (using s: My_Struct) {
//^^^^^^^ entity.name.function.jai
//        ^^ keyword.operator.assignment.jai
//           ^ punctuation.section.parameters.begin.jai
//            ^^^^^ keyword.other.jai
//                  ^ variable.parameter.jai
//                   ^ keyword.operator.assignment.jai
//                     ^^^^^^^^^ storage.type.jai
//                              ^ punctuation.section.parameters.end.jai
}

multi_line_func_0 :: (
	my_param_0: Abcdefe,
	my_param_1: [] float) -> string
{
	
}

multi_line_func_1 :: (my_param_0: Abcdefe,
	my_param_1: [] float
	) -> string
{
	
}

multi_line_func_1(f, 4);

  My_Struct :: struct {
//^^^^^^^^^ variable.other.jai
//          ^^ keyword.operator.assignment.jai
//             ^^^^^^ storage.type.jai
//                    ^ meta.block.jai punctuation.section.block.begin.jai
  member: float;
//^^^^^^ variable.other.jai
//      ^ keyword.operator.assignment.jai
//        ^^^^^ storage.type.jai
//             ^ punctuation.terminator.jai
  }
//^ meta.block.jai punctuation.section.block.end.jai

  my_struct := My_Struct.{0.3};
//^^^^^^^^^ variable.other.jai
//          ^^ keyword.operator.assignment.jai
//             ^^^^^^^^^ storage.type.jai
//                      ^ punctuation.accessor.jai
//                       ^ punctuation.section.block.begin.jai
//                        ^^^ constant.numeric.jai
//                           ^ punctuation.section.block.end.jai
//                            ^ punctuation.terminator.jai
//^^^^^^^^^^^^^^^^^^^^^^ meta.variable.jai

// rwtodo: annotate
operator + :: (a: My_Struct, b: My_Struct) -> My_Struct {
  out : My_Struct = ---;
  out.member = a.member + b.member;
  return out;
}

// rwtodo: annotate
operator += :: (a: My_Struct, b: float) -> int {
  return 23_5;
}

  fun :: (x: int) -> first: string = "Hello", second: string = "Sailor!" {
//^^^ entity.name.function.jai
//    ^^ keyword.operator.assignment.jai
//       ^ punctuation.section.parameters.begin.jai
//        ^ variable.parameter.jai
//         ^ keyword.operator.assignment.jai
//           ^^^ storage.type.jai
//              ^ punctuation.section.parameters.end.jai
//                ^^ keyword.other.jai
//                   ^^^^^ variable.other.jai
//                        ^ keyword.operator.assignment.jai
//                          ^^^^^^ storage.type.jai
//                                 ^ keyword.operator.assignment.jai
//                                   ^^^^^^^ string.quoted.double.jai
//                                          ^ punctuation.separator.jai
//                                                                       ^ meta.block.jai
    if x == 0 return;
    if x == 1 return "Simple";
    if x == 2 return "Simple", "Simon";
    if x == 3 return second = "Simple", first = "Simon";

    return second = "Dolly";
}

varfunc := ()
{
  
}

// an enum found in Compiler.jai
  output_type : enum u8 {
//^^^^^^^^^^^ variable.other.jai
//            ^ keyword.operator.assignment.jai
//              ^^^^ storage.type.jai
//                   ^^ storage.type.jai
//                      ^ meta.block.jai punctuation.section.block.begin.jai
    NO_OUTPUT       :: 0;
//  ^^^^^^^^^ variable.other.jai
//                  ^^ keyword.operator.assignment.jai
//                     ^ constant.numeric.jai
//                      ^ punctuation.terminator.jai
    EXECUTABLE      :: 1;
//  ^^^^^^^^^^ variable.other.jai
//                  ^^ keyword.operator.assignment.jai
//                     ^ constant.numeric.jai
//                      ^ punctuation.terminator.jai
    DYNAMIC_LIBRARY :: 2;
//  ^^^^^^^^^^^^^^^ variable.other.jai
//                  ^^ keyword.operator.assignment.jai
//                     ^ constant.numeric.jai
//                      ^ punctuation.terminator.jai
    STATIC_LIBRARY  :: 3;
//  ^^^^^^^^^^^^^^ variable.other.jai
//                  ^^ keyword.operator.assignment.jai
//                     ^ constant.numeric.jai
//                      ^ punctuation.terminator.jai
  } = .EXECUTABLE;
//^ meta.block.jai punctuation.section.block.end.jai
//    ^ punctuation.accessor.jai
//     ^^^^^^^^^^ variable.other.jai
//               ^ punctuation.terminator.jai

a_mathy_procedure :: (m: Matrix4, v: Vector3) {
  mult_once := (m * make_vector4(v, 1.0)).xyz;
//^^^^^^^^^ variable.other.jai
//                                        ^^^ variable.other.jai
//                                       ^ punctuation.accessor.jai
  mult_twice := (m * make_vector4(mult_once, 1.0)).xyz;
//^^^^^^^^^^ variable.other.jai
//                                                ^ punctuation.accessor.jai
  a := 5 % 24;
}

// Copied from Compiler.jai.
  compiler_create_workspace  :: (name := "") -> Workspace #compiler;
//^^^^^^^^^^^^^^^^^^^^^^^^^ entity.name.function.jai
//                                                        ^^^^^^^^^ meta.preprocessor.jai
  compiler_destroy_workspace :: (w: Workspace) #compiler;
//^^^^^^^^^^^^^^^^^^^^^^^^^^ entity.name.function.jai

proc :: inline () {
  write_string(ifx value then "true" else "false");
}

  proc_no_params :: (   ) {
//^^^^^^^^^^^^^^ entity.name.function.jai
//               ^^ keyword.operator.assignment.jai
//                  ^ punctuation.section.parameters.begin.jai
//                      ^ punctuation.section.parameters.end.jai
  }
  
  
  
main :: () {
  build_options := get_build_options();
  build_options.output_type = .NO_OUTPUT;
  set_build_options(build_options);
  
  for index: 0..7 {
//^^^ keyword.control.jai
//    ^^^^^ variable.other.jai
//         ^ keyword.operator.assignment.jai
//           ^ constant.numeric.jai
//            ^^ keyword.operator.jai
//              ^ constant.numeric.jai
  }
  
  print("A is of type %, value %.\n", type_of(local_var), local_var);
//^^^^^ meta.function-call.jai
//      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ string.quoted.double.jai
//                    ^ constant.other.placeholder.jai
//                             ^ constant.other.placeholder.jai
//                               ^^ constant.character.escape.jai
//                                    ^^^^^^^ meta.function-call.jai
//                                                                  ^ punctuation.terminator.jai

  my_var_123 := a_mathy_procedure(.{}, .{});
//^^^^^^^^^^ variable.other.jai
//           ^^ keyword.operator.assignment.jai
//              ^^^^^^^^^^^^^^^^^ variable.function.jai
//              ^^^^^^^^^^^^^^^^^ meta.function-call.jai
//                                         ^ punctuation.terminator.jai
//^^^^^^^^^^^^^^^^^^^^^^^^ meta.variable.jai
}

#run main();