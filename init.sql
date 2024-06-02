Create table classes(class_id serial, repo_id serial, class text, constraint fk_key FOREIGN KEY(repo_id) references repos(repo_id), PRIMARY KEY(class_id));
Create table file_name(file_id serial, repo_id serial, file text, constraint fk_key FOREIGN KEY(repo_id)
 references repos(repo_id), PRIMARY KEY(file_id));
Create table function_metadata(function_id serial, repo_id serial, file_id serial, class_id serial, function_name text, code text);
Create table function_arguments(argument_id serial, function_id serial, arg text);