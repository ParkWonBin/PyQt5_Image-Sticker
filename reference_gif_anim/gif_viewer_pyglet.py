import pyglet

ani = pyglet.image.load_animation('earth.gif')
animsprite = pyglet.sprite.Sprite(ani)
w = animsprite.width
h = animsprite.height

window = pyglet.window.Window(width=w, height=h, resizable=True)

r,g,b,alpha = 0.5,0.5,0.5,0.5
pyglet.gl.glClearColor(r,g,b,alpha)

@window.event
def on_draw():
    window.clear()
    animsprite.draw()

pyglet.app.run()