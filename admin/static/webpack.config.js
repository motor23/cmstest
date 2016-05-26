var path = require('path');
var webpack = require("webpack");
var config = {
    entry: path.join(__dirname, 'src', 'js', 'index.js'),
    output: {
        path: path.join(__dirname, 'build'),
        filename: 'bundle.js'
    },
    plugins: [
        //new webpack.optimize.DedupePlugin(),
        //new webpack.ContextReplacementPlugin(/moment[\/\\]locale$/, /ru/)
    ],
    module: {
        loaders: [
            {
                test: /\.js$/,
                loader: 'babel',
                query: {
                    presets: [
                        require.resolve('babel-preset-es2015'),
                        require.resolve('babel-preset-react'),
                        require.resolve('babel-preset-stage-0')
                    ]
                },
                include: [
                    path.join(__dirname, 'src', 'js'),
                    path.join(__dirname, 'node_modules')
                ],
                exclude: /node_modules/
            },
            {
                test: /\.css/,
                loader: 'style-loader!css-loader!postcss-loader'
            }
        ],
        noParse: /\.min\.js/
    },
    devtool: 'source-map'
};


module.exports = config;