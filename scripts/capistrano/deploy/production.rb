set :db_config, 'production.database.yml'
#set :rvm_ruby_string, '1.9.3@production'
set :application_cmd, "codesample_production"
set :rvm_type, :user
server "example.com", :web, :app, :db, primary: true
set :repository,  "ssh://git@repo.example.com/codesamples/codesample.git"
set :rails_env, "production"
set :branch, "master"
