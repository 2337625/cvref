require 'rails_helper'

RSpec.describe "static_pages/new", type: :view do
  before(:each) do
    assign(:static_page, StaticPage.new(
      :title => "MyString",
      :content => "MyText"
    ))
  end

  it "renders new static_page form" do
    render

    assert_select "form[action=?][method=?]", static_pages_path, "post" do

      assert_select "input[name=?]", "static_page[title]"

      assert_select "textarea[name=?]", "static_page[content]"
    end
  end
end
