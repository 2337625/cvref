const { environment } = require('@rails/webpacker')
//environment.loaders.prepend('url', url) //this is not loading

const typescript =  require('./loaders/typescript')

//CSS
const merge = require('webpack-merge')
const myCssLoaderOptions = {
  modules: true,
  sourceMap: true,
  localIdentName: '[name]__[local]___[hash:base64:5]'
}
const CSSLoader = environment.loaders.get('css').use.find(el => el.loader === 'css-loader')
CSSLoader.options = merge(CSSLoader.options, myCssLoaderOptions)

//typescript
environment.loaders.append('typescript', typescript)


module.exports = environment
