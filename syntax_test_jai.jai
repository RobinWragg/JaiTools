// SYNTAX TEST "Packages/JaiToolsDev/Jai.sublime-syntax"

  #import "Basic";
//^^^^^^^ keyword.control.import.jai
//        ^^^^^^^ string.quoted.double.jai
//               ^ punctuation.terminator.jai

THE_STRING :: #string DONE
//            ^^^^^^^ meta.preprocessor.jai
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

  my_func_1 :: (my_param: int) {
//^^^^^^^^^ entity.name.function.jai
//          ^^ keyword.operator.assignment.jai
//             ^ punctuation.section.parameters.begin.jai
//              ^^^^^^^^ variable.parameter.jai
//                      ^ keyword.operator.assignment.jai
//                        ^^^ storage.type.jai
//                           ^ punctuation.section.parameters.end.jai
//                             ^ meta.block.jai
  }
//^ meta.block.jai punctuation.section.block.end.jai

  my_func_1 :: (my_param: int) {
//^^^^^^^^^ entity.name.function.jai
//          ^^ keyword.operator.assignment.jai
//             ^ punctuation.section.parameters.begin.jai
//              ^^^^^^^^ variable.parameter.jai
//                      ^ keyword.operator.assignment.jai
//                        ^^^ storage.type.jai
//                           ^ punctuation.section.parameters.end.jai
//                             ^ meta.block.jai
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
    return "ewf", 354;
//  ^^^^^^ keyword.control.jai
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
//^^^^^^^^^^^^^^^^^ entity.name.function.jai
//                  ^^ keyword.operator.assignment.jai
//                     ^ punctuation.section.parameters.begin.jai
  my_param_0: Abcdefe,
//^^^^^^^^^^ variable.parameter.jai
//          ^ keyword.operator.assignment.jai
//            ^^^^^^^ storage.type.jai
//                   ^ punctuation.separator.jai
  my_param_1: [] float) -> string
//^^^^^^^^^^ variable.parameter.jai
//          ^ keyword.operator.assignment.jai
//            ^ punctuation.section.brackets.begin.jai
//             ^ punctuation.section.brackets.end.jai
//               ^^^^^ storage.type.jai
//                    ^ punctuation.section.parameters.end.jai
//                      ^^ keyword.other.jai
//                         ^^^^^^ storage.type.jai
{}

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

// todo: annotate
operator + :: (a: My_Struct, b: My_Struct) -> My_Struct {
  out : My_Struct = ---;
  out.member = a.member + b.member;
  return out;
}

// todo: annotate
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
//^^^^^^^ entity.name.function.jai
//        ^^ keyword.operator.assignment.jai
//           ^ punctuation.section.parameters.begin.jai
//            ^ punctuation.section.parameters.end.jai
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

// Non-anonymous version
  Output_Type :: enum u8 {
//^^^^^^^^^^^ variable.other.jai
//            ^^ keyword.operator.assignment.jai
//               ^^^^ storage.type.jai
//                    ^^ storage.type.jai
//                       ^ meta.block.jai punctuation.section.block.begin.jai
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

  proc_inline :: inline () {
//^^^^^^^^^^^ entity.name.function.jai
//            ^^ keyword.operator.assignment.jai
//               ^^^^^^ keyword.other.jai
  f := ifx value then "true" else "false";
//     ^^^ keyword.control.jai
//               ^^^^ keyword.control.jai
//                    ^^^^^^ string.quoted.double.jai
//                           ^^^^ keyword.control.jai
//                                ^^^^^^^ string.quoted.double.jai

  write_string(ifx value then "true" else "false");
//^^^^^^^^^^^^ meta.function-call.jai
//             ^^^ keyword.control.jai
//                       ^^^^ keyword.control.jai
//                            ^^^^^^ string.quoted.double.jai
//                                   ^^^^ keyword.control.jai
//                                        ^^^^^^^ string.quoted.double.jai
}

  proc_no_params :: (   ) {
//^^^^^^^^^^^^^^ entity.name.function.jai
//               ^^ keyword.operator.assignment.jai
//                  ^ punctuation.section.parameters.begin.jai
//                      ^ punctuation.section.parameters.end.jai
  }

  info_flags : enum_flags u32 { // defaults to 0, which means none of the choices below.
//^^^^^^^^^^^^^^^^^^^^^^^ meta.variable.jai
//                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ comment.line.jai
      POLYMORPH_MATCH       :: 0x1;
//    ^^^^^^^^^^^^^^^ variable.other.jai
//                             ^^^ constant.numeric.jai
      POLYMORPH_DEDUPLICATE :: 0x2;
      AUTO_VALUE_BAKE       :: 0x4;
  }
  
  Another_Struct : struct { // defaults to 0, which means none of the choices below.
//^^^^^^^^^^^^^^ meta.variable.jai
//                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ comment.line.jai
  
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
  
  x_tris :: Vector3.[
//          ^^^^^^^ storage.type.jai
//                 ^ punctuation.accessor.jai
//                  ^ punctuation.section.brackets.begin.jai
    Vector3.{1.0, 0.0, 0.0}, Vector3.{}
//  ^^^^^^^ storage.type.jai
//         ^ punctuation.accessor.jai
//          ^ punctuation.section.block.begin.jai
//                        ^ punctuation.section.block.end.jai
//                           ^^^^^^^ storage.type.jai
  ];
//^ punctuation.section.brackets.begin.jai
// ^ punctuation.terminator.jai
}

// todo: annotate
platform_clear : (colorrr: v3) -> () : clear;

render_submit :: (sub: Submission, matrix := matrix4_identity()) {
  master_matrix := get_master_matrix();
  submit(sub, master_matrix);
}

get_path_of_running_executable :: () -> string /* Temporary Storage */ {
//                                             ^^^^^^^^^^^^^^^^^^^^^^^ comment.block.jai
    BUFFER_SIZE :: 4096;   // @StaticBuffer @Robustness
    buf: [BUFFER_SIZE] u8;

    length := readlink("/proc/self/exe", buf.data, BUFFER_SIZE);
    if length < 0 return "";

    out: string;
    out.data = Basic.alloc(length, Basic.__temporary_allocator);
    out.count = length;
    memcpy(out.data, buf.data, length);

    return out;
}

log_error :: (format_string: string, args: .. Any) {
//                                         ^^ keyword.operator.jai
}

// from Matrix.jai
inverse :: (m: Matrix4) -> Matrix4 #must, bool {
//                                 ^^^^^ meta.preprocessor.jai
//                                      ^ punctuation.separator.jai
//                                        ^^^^ storage.type.jai
}

// From Basic/module.jai
Construct :: (memory: *void, $T: Type) {
    ini :: initializer_of(T);

    #if ini {
        inline ini(memory);
//      ^^^^^^ keyword.other.jai
    } else {
        memset(memory, 0, size_of(T));
    }
}

// Basic parameterized struct
  MyParamStruct :: struct (param1: int, param2: float) {
//^^^^^^^^^^^^^ variable.other.jai
//              ^^ keyword.operator.assignment.jai
//                        ^ punctuation.section.parameters.begin.jai
//                         ^^^^^ variable.parameter.jai
//                               ^ keyword.operator.assignment.jai
//                                 ^^^ storage.type.jai
//                                    ^ punctuation.separator.jai
//                                      ^^^^^^ variable.parameter.jai
//                                            ^ keyword.operator.assignment.jai
//                                              ^^^^^ storage.type.jai
//                                                   ^ punctuation.section.parameters.end.jai
//                                                     ^ meta.block.jai
  }

  MatrixType :: struct(
//^^^^^^^^^^ variable.other.jai
//           ^^ keyword.operator.assignment.jai
//              ^^^^^^ storage.type.jai
//                    ^ punctuation.section.parameters.begin.jai
    matrix_type: Type, 
//  ^^^^^^^^^^^ variable.parameter.jai
    data_type: Type,
    N: int,
    M: int,
    flags: MATRIX_FLAGS,
    get: (m: matrix_type, int, int) -> data_type,
//       ^ punctuation.section.parameters.begin.jai
//                                ^ punctuation.section.parameters.end.jai
    set: (m: *matrix_type, int, int, data_type) -> ()
//       ^ punctuation.section.parameters.begin.jai
//                                            ^ punctuation.section.parameters.end.jai
  ){}
//^ punctuation.section.parameters.end.jai
// ^ meta.block.jai punctuation.section.block.begin.jai
//  ^ meta.block.jai punctuation.section.block.end.jai


#run main();
