set :default_shell, :bash
set :stages, %w(staging production)
set :default_stage, "production"
# Load RVM's capistrano plugin.
require 'rvm/capistrano'
require 'capistrano/ext/multistage'
require 'sidekiq/capistrano'
#require 'bundler/capistrano'

set :application, "example.com"
set :servername, "192.168.122.10"
set :user, "deployer"
set :scm_username, 'git'
set :deploy_via, :remote_cache
set :deploy_to, "/var/www/sites/#{application}"
set :copy_exclude, [ '.git' ]
set :use_sudo, true
set :keep_releases, 3
after "deploy:update", "deploy:cleanup" 

set :scm, "git"
set :repository_cache, "cached_copy"

default_run_options[:pty] = true
ssh_options[:auth_methods] = ['publickey']  
ssh_options[:keys] = [File.join(ENV["HOME"], ".ssh", "root"),File.join(ENV["HOME"], ".ssh", "id_rsa")]

after "deploy", "deploy:cleanup"


task :symlink_config, roles: :app do
  run "mkdir -p #{latest_release}/config"
  #run "cp #{release_path}/config/#{db_config} #{shared_path}/config/#{db_config}"
  run "ln -nfs #{shared_path}/config/#{db_config} #{latest_release}/config/database.yml"
  run "mkdir -p #{shared_path}/tmp"
  run "ln -nfs #{shared_path}/tmp #{latest_release}/tmp"
  run "ln -nfs #{shared_path}/uploads #{latest_release}/public/uploads"
  run "ln -nfs #{shared_path}/system #{latest_release}/public/system"
  if rails_env == 'production'
    run "ln -nfs #{shared_path}/assets #{latest_release}/public/assets"
  else
    #run "rm -rf #{latest_release}/public/assets"
  end
end

  namespace :deploy do
  %w[start stop restart upgrade].each do |command|
    desc "#{command} unicorn server"
    task command, :roles => :app, :except => { :no_release => true } do
      sudo "chmod a+x /etc/init.d/unicorn_#{application_cmd}"
      sudo "/etc/init.d/unicorn_#{application_cmd} #{command}"
    end
  end

  namespace :assets do
    task :precompile, :roles => :web, :except => { :no_release => true } do
      if rails_env == 'production'
        run_locally "RAILS_ENV=#{rails_env} && bundle exec rake assets:clean"
        run_locally "RAILS_ENV=#{rails_env} && bundle exec rake assets:precompile"
        run_locally "rsync -av ./public/assets/ #{user}@#{servername}:#{shared_path}/assets/;"
      end
    end
    after "deploy:symlink_config", "deploy:assets:precompile"
  end

  task :setup_config, roles: :app do
    run "ln -nfs #{current_path}/config/unicorn_init.sh /etc/init.d/unicorn_#{application_cmd}"
    run "chmod a+x /etc/init.d/unicorn_#{application_cmd}"
    run "mkdir -p #{shared_path}/config"
    #put File.read("#{shared_path}/config/#{db_config}"), "#{release_path}/config/#{db_config}"
    #puts "Now edit the config files in #{shared_path}/config."
  end
  after "deploy:cold", "deploy:setup_config"

  after "deploy:create_symlink", "symlink_config"

  desc "Make sure local git is in sync with remote."
  task :check_revision, roles: :web do
    unless `git rev-parse HEAD` == `git rev-parse origin/#{branch}`
      puts "WARNING: HEAD is not the same as origin/#{branch}"
      puts "Run `git push` to sync changes."
      exit
    end
  end
  before "deploy", "deploy:check_revision"

end
