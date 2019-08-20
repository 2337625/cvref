source 'https://rubygems.org'
git_source(:github) { |repo| "https://github.com/#{repo}.git" }

ruby '2.5.1'

# Bundle edge Rails instead: gem 'rails', github: 'rails/rails'
gem 'rails', '~> 5.2.0'

# i18n + l10n
# url: https://www.justinweiss.com/articles/rails-i18n-3-quick-tips-and-1-crazy-abuse/
gem 'rails-i18n'
# Use sqlite3 as the database for Active Record
gem 'sqlite3'
# Use Puma as the app server
gem 'puma', '~> 3.11'
# Build JSON APIs with ease. Read more: https://github.com/rails/jbuilder
# gem 'jbuilder', '~> 2.5'
# Use Redis adapter to run Action Cable in production
# gem 'redis', '~> 4.0'

# Use ActiveModel has_secure_password
gem 'bcrypt', '~> 3.1.7'

# Escape utils - faster html escaping
# url: https://github.com/brianmario/escape_utils
# @TODO: later install and benchmark
#gem 'escape_utils'

# Faster blank?
# url: https://github.com/SamSaffron/fast_blank
gem 'fast_blank'

# Oj - fast json serializer
# url: https://github.com/ohler55/oj
gem 'oj'

# Paranoia - delete handling
# https://github.com/rubysherpas/paranoia
# Aug 04, not compatible with activerecord 5.2.0
#gem "paranoia", github: "rubysherpas/paranoia", branch: "rails5"

# Reduces boot times through caching; required in config/boot.rb
gem 'bootsnap', '>= 1.1.0', require: false

# Use Rack CORS for handling Cross-Origin Resource Sharing (CORS), making cross-origin AJAX possible
# gem 'rack-cors'

# Templating engine
# url: https://github.com/slim-template/slim-rails
# cheatsheet: https://devhints.io/slim
gem 'slim-rails'

# Web packer
# url: https://github.com/rails/webpacker
# tutorial:https://medium.com/statuscode/introducing-webpacker-7136d66cddfb
#gem 'webpacker', '~> 3.5'
# OR to try out 4.x pre-release
gem 'webpacker', '>= 4.0.x'
#yarn add @rails/webpacker@4.0.0-pre.2

# Routes for i18n
# url: https://github.com/enriclluelles/route_translator
# tutorial: https://www.leanpanda.com/blog/2015/09/12/alternate-sitemap/
# testing: https://anadea.info/blog/testing-localization-with-cucumber
gem 'route_translator'

# Oga instead of Nokogiri - but rails requires
# url: http://www.mikeperham.com/2016/02/09/kill-your-dependencies/
# gem 'oga'

# SEO URLs
# url: gem 'friendly_id', '~> 5.2.0'
# rails g friendly_id
gem 'friendly_id'

# Content translation
# url: https://github.com/shioyama/mobility
# rails generate mobility:install
gem 'mobility', '~> 0.7.6'
# SEO URL translation support
# url: https://github.com/shioyama/friendly_id-mobility
# rails generate mobility:install
# rails g friendly_id
# rails db:migrate
gem 'friendly_id-mobility', '~> 0.5.4'

# Environment variables
# url: https://github.com/railsconfig/config
# rails g config:install
gem 'config'

# Uniquify - unique tokens
# url: https://github.com/ryanb/uniquify
gem 'uniquify'

# Authentication
# url: https://github.com/plataformatec/devise#starting-with-rails
# rails g devise:install
#  rails generate devise MODEL # User
gem 'devise'

# Translate Auth
# url: https://github.com/tigrish/devise-i18n
# railsg g devise:i18n:views user
# rails g devise:i18n:locale de
gem 'devise-i18n'

# Code layout/design
# tutorials: https://web.archive.org/web/20130712014326/
# http://blog.andywaite.com/2012/12/23/exploring-concerns-for-rails-4/
# https://stackoverflow.com/questions/14541823/how-to-use-concerns-in-rails-4

# Modular views - View abstraction via Cells
# url: http://trailblazer.to/gems/cells/rails.html
# description: https://github.com/trailblazer/cells
# tutorial: https://www.sitepoint.com/introduction-to-cells-a-better-view-layer-for-rails/
# code structure: https://robots.thoughtbot.com/refactoring-replace-conditional-with-polymorphism
# gem 'cells-rails'
# gem 'cells-slim'

# Enumerize
# url: https://github.com/brainspec/enumerize
# gem 'enumerize'

# Country select
# url: https://github.com/onomojo/i18n_country_select
gem 'i18n_country_select'

# Goldiloder optimize queries
# url: https://github.com/salsify/goldiloader
# gem 'goldiloader'

# Act as taggable
# url: gem 'acts-as-taggable-on', '~> 6.0'
# url: https://github.com/mbleigh/acts-as-taggable-on
# migrations for the latest versions :
# rails acts_as_taggable_on_engine:install:migrations
gem 'acts-as-taggable-on', '~> 6.0'

# meta-tags for html header
# url: https://github.com/kpumuk/meta-tags
# rails generate meta_tags:install
gem 'meta-tags'

# Mercury html5 editor - cool for static pages
# url: https://github.com/jejacks0n/mercury
# gem 'mercury-rails'

# Koala - Facebook graph_api
# url: https://github.com/arsduo/koala
# gem 'koala'



group :development, :test do
  # Call 'byebug' anywhere in the code to stop execution and get a debugger console
  gem 'byebug', platforms: [:mri, :mingw, :x64_mingw]
  gem 'pg'

  # @author: added
  gem 'rspec-rails'
  gem 'timecop'
end

group :development do
  gem 'listen', '>= 3.0.5', '< 3.2'
  # Spring speeds up development by keeping your application running in the
  # background. Read more: https://github.com/rails/spring
  gem 'spring'
  gem 'spring-watcher-listen', '~> 2.0.0'

  # @author: mynick
  # url: https://github.com/hothero/awesome-rails-gem#user
  # @TODO: add more cool gems
  # Performance
  # url: https://marianposaceanu.com/articles/improve-rails-performance-by-adding-a-few-gems

  # Below are all original commented out

  # Use ActiveStorage variant
  # gem 'mini_magick', '~> 4.8'

  # Use Capistrano for deployment
  # gem 'capistrano-rails', group: :development

  # @author: added lines below
  #
  # gem 'rollbar'
  # gem 'lograge'
  # gem 'sidekiq'
  # gem 'octokit'

  # Gems we don't need in app but in env only
  # Foreman to spin all devservers
  gem 'foreman', require: false

  # To convert erb2slim
  # url: https://coderwall.com/p/bn1akg/erb2slim-convert-erb-to-slim
  gem 'html2slim', require: false
  gem 'html2haml', require: false
  gem 'haml2slim', require: false

  # Benchmark
  # url: https://www.ombulabs.com/blog/rails/ruby/how-to-use-any-gem-in-production-console.html
  #gem 'benchmark-ips'

  # Application profiling for n+1 queries
  # url: https://github.com/flyerhzm/bullet
  #gem 'bullet'

  # Pretty print
  #gem 'awesome-print'

  # Pretty Errors
  # url: https://github.com/charliesome/better_errors
  #gem "better_errors"
  #gem "binding_of_caller"

end

# group :production do
#   # @TODO: Optimize production env
#   # url: https://github.com/ankane/rails-best-practices
#   gem 'cell-rails'
# end


# Windows does not include zoneinfo files, so bundle the tzinfo-data gem
gem 'tzinfo-data', platforms: [:mingw, :mswin, :x64_mingw, :jruby]
