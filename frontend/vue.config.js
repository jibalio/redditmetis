const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
// const UglifyJsPlugin = require('uglifyjs-webpack-plugin'); // This doesn't minify ES6 anymore

const TerserPlugin = require('terser-webpack-plugin');

var webpack = require('webpack');


var production = {
    publicPath: "/rmstatic/spa",
    // outputDir: "../app_redditmetis/static/spa",
    // relative to outputDir
    // assetsDir: "spa_assets",
    configureWebpack: {
        plugins: [
            new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/),
            new BundleAnalyzerPlugin(),
        ],
        optimization: {
            minimize:true,
            minimizer: [new TerserPlugin()],
        }
    },
};

var dev = {
    configureWebpack: {
        
    },
};


function config() {
    if (process.env.NODE_ENV === 'production') {
        return production;
    } else {
        return dev;
    }
}

module.exports = config();