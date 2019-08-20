class StaticPage < ApplicationRecord
  extend Mobility
  translates :title,    type: :string
  translates :content,  type: :text
  translates :slug,     type: :string
  # https://github.com/shioyama/friendly_id-mobility
  translates :slug, :title, dirty = true

  extend FriendlyId
  friendly_id :title, use: [:history, :mobility]

  acts_as_taggable # Alias for acts_as_taggable_on :tags
  acts_as_taggable_on :category, :tag_words

  has_many_attached :images, dependent: :destroy

  def to_meta_tags
    title = 'my tagish title'
    description = 'summarish picish'
  end
end
