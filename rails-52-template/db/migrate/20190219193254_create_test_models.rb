class CreateTestModels < ActiveRecord::Migration[5.2]
  def change
    create_table :test_models do |t|
      t.string :name
      t.text :content
      t.text :something

      t.timestamps
    end
  end
end
