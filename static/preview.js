const params = new URLSearchParams(window.location.search)
const url = params.get('url')
console.log('url: ' + url)

const getClips = async () => {
  const response = await fetch(`/clips?url=${encodeURI(url)}`)
  if (!response.ok) {
    console.error('Failed to fetch clips')
    return null
  }
  return await response.json()
}

const displayClips = async () => {
  const clips = await getClips()
  if (clips === null) {
    return
  }
  console.log(clips)

  const content = document.body.getElementsByClassName('content')[0]
  if (content === null) return
  const svg =
    '<svg xmlns="http://www.w3.org/2000/svg" height="0.75em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path fill="#ffffff" d="M216 0h80c13.3 0 24 10.7 24 24v168h87.7c17.8 0 26.7 21.5 14.1 34.1L269.7 378.3c-7.5 7.5-19.8 7.5-27.3 0L90.1 226.1c-12.6-12.6-3.7-34.1 14.1-34.1H192V24c0-13.3 10.7-24 24-24zm296 376v112c0 13.3-10.7 24-24 24H24c-13.3 0-24-10.7-24-24V376c0-13.3 10.7-24 24-24h146.7l49 49c20.1 20.1 52.5 20.1 72.6 0l49-49H488c13.3 0 24 10.7 24 24zm-124 88c0-11-9-20-20-20s-20 9-20 20 9 20 20 20 20-9 20-20zm64 0c0-11-9-20-20-20s-20 9-20 20 9 20 20 20 20-9 20-20z"/></svg>'
  for (let clip of clips) {
    console.log(clip)
    const title = clip.split('/').pop()
    const node = document.createElement('div')
    node.innerHTML = `<div class="title"><a download href=${clip} class="clip-title"><span style="text-decoration:underline;">${title}</span>  ${svg}</a></div><video width="640" height="480" controls><source src="${clip}" type="video/mp4">Your browser does not support the video tag.</video>`
    content.appendChild(node)
  }
}

displayClips()
