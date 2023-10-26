const path = require('path')

module.exports = {
  mode: 'development',
  devtool: 'source-map',
  entry: {
    quill: './notes.js',
  },
  output: {
    globalObject: 'self',
    path: path.resolve(__dirname, './dist/'),
    filename: '[name].bundle.js',
    publicPath: './dist/'
  },
  devServer: {
    contentBase: path.join(__dirname),
    compress: true,
    publicPath: '/dist/'
  }
}
