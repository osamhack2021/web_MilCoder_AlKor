let date = require('moment')().format('YYYYMMDD')
let version = `"${date}"`

console.log(`current version is ${version}`)

module.exports = {
  NODE_ENV: '"development"',
  VERSION: version,
}
