var dir = null
var gameLoop = null
const n = 12
var gameSpeed = 1

var apple = null
var head = null

const params = new URLSearchParams(window.location.search)
const url = params.get('url')
// console.log('url: ' + url)

let pingStatus = 0
var num = 0
let ping = setInterval(() => {
  ;(async function () {
    const response = await fetch(
      `/status?url=${encodeURIComponent(url)}&num=${num++}`
    )
    if (!response.ok) {
      pingStatus = -1
      clearInterval(ping)
      return
    }
    const text = await response.text()
    if (text === '1') {
      window.open(`/preview?url=${encodeURIComponent(url)}`, '_self')
    }
  })()
}, 1000)

const restart = () => {
  if (gameLoop) {
    clearInterval(gameLoop)
  }
  setTimeout(() => {
    dir = null
    head = new Snake(6, 6)
  }, 2000)
}

class Snake {
  constructor(x, y) {
    this.x = x
    this.y = y
    this.length = 1
    this.next = null
  }

  grow() {
    const end = this.getEnd()
    this.growTo(end[0], end[1])
  }

  growTo(x, y) {
    this.length++
    if (!this.next) {
      this.next = new Snake(x, y)
    } else {
      this.next.growTo(x, y)
    }
  }

  getEnd() {
    if (this.next) return this.next.getEnd()
    return [this.x, this.y]
  }

  moveTo(x, y) {
    if (this.next) {
      this.next.moveTo(this.x, this.y)
    }
    this.x = x
    this.y = y
  }

  move(dir) {
    let dx = 0
    let dy = 0
    if (dir === 'w') dy = -1
    if (dir === 'a') dx = -1
    if (dir === 's') dy = 1
    if (dir === 'd') dx = 1
    if (this.next) {
      this.next.moveTo(this.x, this.y)
    }
    this.x += dx
    this.y += dy
    if (this.next) {
      // console.log(
      // `head: (${this.x}, ${this.y}); next: (${this.next.x}, ${this.next.y})`
      // )
    }
    if (this.next && this.next.contains(this.x, this.y)) {
      console.log('clearInterval')
      restart()
    }
    if (this.x === apple[0] && this.y === apple[1]) {
      this.grow()
      apple = generateAppleCoordinates()
    }
    if (this.x < 0 || this.x >= n || this.y < 0 || this.y >= n) {
      restart()
    }
  }

  contains(x, y) {
    if (this.x == x && this.y == y) return true
    if (this.next !== null) return this.next.contains(x, y)
    return false
  }

  size() {
    if (this.next) return 1 + this.next.size()
    else return 1
  }
}

head = new Snake(6, 6)
const generateAppleCoordinates = () => {
  let x = null,
    y = null
  while (x == null || y == null) {
    x = Math.floor(Math.random() * n)
    y = Math.floor(Math.random() * n)
    if (head.contains(x, y)) {
      x = null
      y = null
    }
  }
  return [x, y]
}
apple = generateAppleCoordinates()

const init = () => {
  const html = document.getElementsByTagName('html').item(0),
    canvas = document.getElementsByTagName('canvas').item(0),
    context = canvas.getContext('2d')

  const resize = () => {
    canvas.width = w = window.innerWidth
    canvas.height = h = window.innerHeight
    context.font = `${h * 0.157894737}px monospace`
    context.textBaseline = 'hanging'
    context.textAlign = 'center'
  }

  const handleKeyDown = key => {
    const temp = dir
    if (['w', 'a', 's', 'd'].includes(key)) {
      dir = key
      // console.log(dir)
      if (temp === null) {
        gameLoop = setInterval(() => {
          console.log('interval')
          head.move(dir)
        }, 200 / gameSpeed)
      }
    }
  }

  const loop = t => {
    context.fillStyle = '#000000'
    context.fillRect(0, 0, w, h)
    context.strokeStyle = '#fff'
    context.lineWidth = 5
    const left = canvas.width / 2 - 300
    const top = canvas.height / 2 - 300
    context.strokeRect(left, top, 600, 600)
    // context.fillStyle = '#0000ff'
    // for (let i = 0; i < n; i++) {
    //   context.fillRect(left + (600 / n) * i, top, 5, 600)
    //   context.fillRect(left, top + (600 / n) * i, 600, 5)
    // }
    let s = head
    context.fillStyle = '#0000ff'
    while (s !== null) {
      context.fillRect(
        left + (600 / n) * s.x,
        top + (600 / n) * s.y,
        600 / n,
        600 / n
      )
      s = s.next
    }

    // Draw apple
    context.fillStyle = '#ff0000'
    context.fillRect(
      left + (600 / n) * apple[0],
      top + (600 / n) * apple[1],
      600 / n,
      600 / n
    )

    if (head.size() === 144) {
      restart()
      gameSpeed += 0.25
    }

    i++
    last = t
    window.requestAnimationFrame(loop)
  }

  let w,
    h,
    last,
    i = 0,
    start = 0

  window.removeEventListener('load', init)
  window.addEventListener('resize', resize)
  window.addEventListener('keydown', e => handleKeyDown(e.key))
  resize()
  html.classList.remove('no-js')
  html.classList.add('js')
  window.requestAnimationFrame(loop)
}

window.addEventListener('load', init)
