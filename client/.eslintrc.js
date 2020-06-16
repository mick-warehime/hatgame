module.exports = {
  "env": {
    "browser": true,
    "es2020": true,
  },
  "extends": [
    "eslint:recommended",
    "plugin:react/recommended",
  ],
  "parserOptions": {
    "ecmaFeatures": {
      "jsx": true,
    },
    "ecmaVersion": 11,
    "sourceType": "module",
  },
  "plugins": [
    "react",
  ],
  "rules": {
    // override default options
    "indent": ["error", 2,],
    "no-cond-assign": ["error", "always",],

    // disable now, but enable in the future
    "one-var": "off", // ["error", "never"]

    // disable
    "init-declarations": "off",
    "no-console": "off",
    "no-inline-comments": "off",
    "no-undef": "off",
  },
};
