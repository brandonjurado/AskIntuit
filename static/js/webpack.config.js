const path = require('path');
module.exports = {
  mode: 'development',
  entry: './app.jsx',
  output: {
    path: path.resolve('./'),
    filename: 'build.js'
  },
  module: {
    rules: [
      { test: /\.css$/,
        use: [
          { loader: "style-loader" },
          { loader: "css-loader" }
        ]
      },
      { test: /\.(s*)css$/,
        use: ['style-loader','css-loader', 'sass-loader']
      },
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: "babel-loader"
      }, {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        loader: "babel-loader",
        query:
        {
          presets:['es2015','react']
        }
      },
      { test: /\.(eot|svg|ttf|woff|woff2)$/, 
        loader: 'file-loader?name=static/js/[name].[ext]'
      },{
        test: /\.(jpg|png)$/,
        use: {
          loader: "url-loader",
          options: {
            limit: 25000,
          },
        },
      },
    ]
  }
}