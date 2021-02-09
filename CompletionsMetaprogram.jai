
// TODO: don't index operator headers
// TODO: linux: 'which' vs 'whereis'

logger: String_Builder;

func :: (param: int) -> float {
  get_pi :: () -> float {
    return 3.14159;
  }
  
  return get_pi() * param;
}

src_lines: [] string;

load_src_lines :: (file_path: string) {
  contents, success := read_entire_file(file_path);
  src_lines = split(contents, "\n");
}

second_workspace: Workspace;

set_all_build_options :: () {
  build_options := get_build_options();
  build_options.output_type = .NO_OUTPUT;
  set_build_options(build_options);
  
  second_workspace = compiler_create_workspace();
  
  sublimecode_build_options := get_build_options(second_workspace);
  sublimecode_build_options.output_type = .NO_OUTPUT;
  set_build_options(sublimecode_build_options);
}

alloc_text_from_node :: (node: *Code_Node) -> string {
  if node.l0 == node.l1 {
    return slice(src_lines[node.l0-1], node.c0-1, node.c1 - node.c0);
  } else {
    first_line := src_lines[node.l0-1];
    first_line = slice(first_line, node.c0-1, first_line.count - (node.c0-1));
    
    last_line := src_lines[node.l1-1];
    last_line = slice(last_line, 0, node.c1-1);
    
    // TODO: handle nodes that span more than two lines.
    if node.l1 - node.l0 > 1 {
      print_to_builder(*logger, "Unhandled node starting at line % due to line spread\n", node.l0);
    }
    
    return join(first_line, last_line);
  }
}

print_proc_header :: (builder: *String_Builder, proc_header: *Code_Procedure_Header) {
  // TODO: Remove contiguous spaces resulting from newlines
  // TODO: Print the sublime json
  
  // TODO: try baking this proc?
  if begins_with(proc_header.name, "-")
    || begins_with(proc_header.name, "+")
    || begins_with(proc_header.name, "*")
    || begins_with(proc_header.name, "/")
    || begins_with(proc_header.name, "<")
    || begins_with(proc_header.name, ">")
    || begins_with(proc_header.name, "&")
    || begins_with(proc_header.name, "|")
    || begins_with(proc_header.name, "~") {
      return;
  }
  
  //
  // Print the entry that will show in the list
  //
  print_to_builder(builder, "['%(", proc_header.name);
  
  for proc_header.arguments {
    if it_index < proc_header.arguments.count-1 {
      print_to_builder(builder, "%, ", alloc_text_from_node(it));
    } else {
      print_to_builder(builder, alloc_text_from_node(it));
    }
  }
  
  print_to_builder(builder, ")");
  
  if proc_header.returns.count > 0 {
    print_to_builder(builder, " -> ");
    
    for proc_header.returns {
      if it_index < proc_header.returns.count-1 {
        print_to_builder(builder, "%, ", alloc_text_from_node(it));
      } else {
        print_to_builder(builder, alloc_text_from_node(it));
      }
    }
  }
  
  //
  // Additional info that will show on the right of the list entry (filename, basically)
  //
  print_to_builder(builder, "\\t %', '", ui_name);
  
  //
  // Print the text that will be insert including completions the user can Tab through
  //
  print_to_builder(builder, "%(", proc_header.name);
  
  for proc_header.arguments {
    if it_index < proc_header.arguments.count-1 {
      print_to_builder(builder, "${%:%}, ", it_index+1, alloc_text_from_node(it));
    } else {
      print_to_builder(builder, "${%:%}", it_index+1, alloc_text_from_node(it));
    }
  }
  
  print_to_builder(builder, ")'],\n");
}

ui_name: string;
sublime_file_path: string;

main :: () {
  cmd_line_args := compiler_get_command_line_arguments();
  
  print("argcount: %\n", cmd_line_args.count);
  print("arg1: %\n", cmd_line_args[0]);
  print("arg2: %\n", cmd_line_args[1]);
  assert(cmd_line_args.count == 2, "Arg 1 must be the UI name of the file. Arg 2 must be the file path.");
  
  ui_name = cmd_line_args[0];
  sublime_file_path = cmd_line_args[1];
  
  set_all_build_options();
  
  // Start the python list declaration
  python_builder: String_Builder;
  print_to_builder(*python_builder, "completions_from_metaprogram = [\n");
  
  load_src_lines(sublime_file_path);
  
  compiler_begin_intercept(second_workspace);
  add_build_file(sublime_file_path, second_workspace);
  
  while true {
      message := compiler_wait_for_message();
      if !message || message.workspace != second_workspace continue;
      
      if message.kind == .CODE_TYPECHECKED {
        typechecked_message := cast(*Compiler_Message_Code_Typechecked) message;
        
        for declaration: typechecked_message.declarations {
          // rwtodo: this is a crap way to filter declarations that aren't in the file we care about.
          if !contains(declaration.filename, sublime_file_path) continue;
          
          if !declaration.root_expression continue;
          
          if declaration.name.count == 0 continue;
          
          print("kind: %\n", declaration.root_expression.kind);
          
          if declaration.root_expression.kind == {
            case .PROCEDURE_HEADER;
              print_proc_header(*python_builder, cast(*Code_Procedure_Header) declaration.root_expression);
          }
        }
      }
      
      if message.kind == .COMPLETE break;
  }
  
  compiler_end_intercept(second_workspace);
  
  print_to_builder(*python_builder, "]\n");
  
  python_list := builder_to_string(*python_builder);
  print(python_list);
}

#run main();

#import "Basic";
#import "Compiler";
#import "String";
#import "File";