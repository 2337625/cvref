set :db_config, 'preheat.database.yml'
set :rvm_ruby_string, "ruby-1.9.3@codesample"
set :rvm_type, :system
server "codesample.preheat.example.com", :web, :app, :db, primary: true
set :repository,  "ssh://git@repo.example.com/codesamples/codesample.git"
set :rails_env, "preheat"
set :branch, "master"
