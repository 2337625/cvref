Rails.application.routes.draw do


  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html

  scope "(:locale)", locale: /en|cs/ do
    root to: 'homepage#index'
    resources :homepage
    devise_for :users
    resources :static_pages, param: :slug, constraints: { slug: /[a-zA-Z0-9-]{0,255}/ }

  end
end
