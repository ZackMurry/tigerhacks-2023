var dir = null
var gameLoop = null
const n = 12

var ax = -1
var ay = -1

const generateAppleCoordinates = () => {
  let x = Math.floor(Math.random() * n)
  let y = Math.floor(Math.random() * n)
}
// todo: spawn apple and grow when eating

class Snake {
  constructor(x, y) {
    this.x = x
    this.y = y
    this.length = 1
    this.next = null
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
    return [x, y]
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
    if (this.x < 0 || this.x >= n || this.y < 0 || this.y >= n) {
      clearInterval(gameLoop)
    }
  }

  contains(x, y) {
    if (this.x == x && this.y == y) return true
    if (this.next !== null) return this.next.contains(x, y)
    return false
  }
}

const head = new Snake(6, 6)

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
      console.log(dir)
      if (temp === null) {
        gameLoop = setInterval(() => {
          console.log('interval')
          head.move(dir)
        }, 200)
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
    context.fillStyle = '#0000ff'
    for (let i = 0; i < n; i++) {
      context.fillRect(left + (600 / n) * i, top, 5, 600)
      context.fillRect(left, top + (600 / n) * i, 600, 5)
    }
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
