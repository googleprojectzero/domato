const fs = require('fs')

let statFiles = []

statFiles = statFiles.concat(fs.readdirSync('./result1/statistic').map(filename => `./result1/statistic/${filename}`))
statFiles = statFiles.concat(fs.readdirSync('./result2/statistic').map(filename => `./result2/statistic/${filename}`))
statFiles = statFiles.concat(fs.readdirSync('./result3/statistic').map(filename => `./result3/statistic/${filename}`))
statFiles = statFiles.concat(fs.readdirSync('./result4/statistic').map(filename => `./result4/statistic/${filename}`))
statFiles = statFiles.concat(fs.readdirSync('./result5/statistic').map(filename => `./result5/statistic/${filename}`))
statFiles = statFiles.concat(fs.readdirSync('./result6/statistic').map(filename => `./result6/statistic/${filename}`))
statFiles = statFiles.concat(fs.readdirSync('./result7/statistic').map(filename => `./result7/statistic/${filename}`))
statFiles = statFiles.concat(fs.readdirSync('./result8/statistic').map(filename => `./result8/statistic/${filename}`))
statFiles = statFiles.concat(fs.readdirSync('./result9/statistic').map(filename => `./result9/statistic/${filename}`))
statFiles = statFiles.concat(fs.readdirSync('./result10/statistic').map(filename => `./result10/statistic/${filename}`))
statFiles = statFiles.concat(fs.readdirSync('./result11').map(filename => `./result11/${filename}`))

const statSize = statFiles.length

const statForArea = (areaName) => {
  const numberOfCorpus = statFiles.length

  const numberOfNonzero = statFiles
    .map(filename => {
      const statData = JSON.parse(fs.readFileSync(filename, 'utf-8'))
      return statData['totalLine'][areaName][0]
    })
    .filter(a => a !== 0)
    .length
  
  const nonzeroDatas = statFiles
  .map(filename => {
    const statData = JSON.parse(fs.readFileSync(filename, 'utf-8'))
    return statData['totalLine'][areaName].length
  })
  .filter(a => a !== 1)
  .reduce((a, b) => a + b)

  const areaLineFirst = statFiles
    .map(filename => {
      const statData = JSON.parse(fs.readFileSync(filename, 'utf-8'))
      return statData['totalLine'][areaName][0]
    })
    .reduce((a, b) => a + b)

  const areaErrorNum = statFiles
    .map(filename => {
      const statData = JSON.parse(fs.readFileSync(filename, 'utf-8'))
      return statData['errorLine'][areaName]
    })
    .filter(a => a[0] !== 0)
    .reduce((a, b) => {
      let longer = a.length < b.length ? b : a
      let shorter = a.length >= b.length ? b : a
      return longer.slice(0, shorter.length).map((a, i) => a + shorter[i]).concat(longer.slice(shorter.length))
    })
  
  let errorSum = 0
  const areaLineShrink = [areaLineFirst].concat(areaErrorNum.map(a => {
    errorSum += a
    return areaLineFirst - errorSum
  }))

  console.log(`${areaName} total document`)
  console.log(numberOfCorpus)
  console.log(`${areaName} nonzero document`)
  console.log(numberOfNonzero)
  console.log(`${areaName} average reduce`)
  console.log(nonzeroDatas / numberOfCorpus)


  console.log(`${areaName} line first`)
  console.log(areaLineFirst)
  console.log(`${areaName} line change`)
  console.log(areaLineShrink)
  console.log(`${areaName} line shrink`)
  console.log(areaErrorNum)
}

statForArea('jsfuzzer')
statForArea('eventhandler1')
statForArea('eventhandler2')
statForArea('eventhandler3')
statForArea('eventhandler4')
statForArea('eventhandler5')

  





