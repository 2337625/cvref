set :db_config, 'stage.database.yml'
set :rvm_ruby_string, :system
#set :rvm_autolibs_flag, "read-only"       # more info: rvm help autolibs
#set :rvm_type, :system
server "codesample.stage.example.com", :web, :app, :db, primary: true
set :repository,  "ssh://git@repo.example.com/codesamples/codesample.git"
set :rails_env, "staging"
set :branch, "master"
set :application_cmd, "codesample_stage"
