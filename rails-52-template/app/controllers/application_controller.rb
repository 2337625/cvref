class ApplicationController < ActionController::Base
  # Devise configuration
  protect_from_forgery
  #before_action :authenticate_user!

  # I18n
  before_action :set_locale

  private
  def set_locale
    I18n.locale = params[:locale] || I18n.default_locale
    Rails.application.routes.default_url_options[:locale]= I18n.locale
  end

  # To include locale to each url
  # url: http://api.rubyonrails.org/v5.2.0/classes/ActionDispatch/Routing/Mapper/Base.html#method-i-default_url_options
  def default_url_options
    { locale: I18n.locale }
  end
end
