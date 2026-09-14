+++
date = '2025-12-08T18:45:56Z'
draft = false
title = 'To Free or Not to Free'
authors = ['davidkschwob']
showAuthor = true
showAuthorBottom = true
showTableOfContents = true
+++

When bad things happen to good free freemium users ...


<!--more-->

## TLDR;

It was a good learning exercise and now I've got a pretty sweet dev sandbox for tinkering.

Having heard about Oracle's _always free_ Cloud Infrastructure ... I felt like
Curious George. I couldn't resist!

I went right over to cloud.oracle.com and singed up for the free trial.
There's a lotta knobs n levers here. Oh my!. Where to start ...

## AI to the rescue ...

"Walk me through setting up an always free tier vps on Oracle OCI"

*BAM!*

I get a _mostly_ correct outline of where to click.

So then we just follow the steps and its up and running.
The site even has a nifty built-in terminal shell that you can use to connect
to the virtual machine:

![Screencap of VPS running on cloud.oracle.com](/img/vps-screenshot.png)


## Doing stuff 

HA! This is great!  
We start doing stuff ...

### helix

```bash
sudo snap install helix --classic
```

Yippee! Now we're talkin'. Fast TUI editor with decent OOTB features built-in.
No more spending all day installing VIM plugins or VS Code extensions.  

![helix editor in acdtion](/img/helix-editor.png)

### nginx

A webserver that also does cool proxy stuff ... more to come on that.

```bash
sudo apt install nginx
```

### certbot

Magically get SSL certs for your personal domain name.

```bash
sudo snap install certbot --classic
```

### hugo

This site is built with hugo. Posts are just a matter of writing a new markdown file under the posts/ folder.

```bash
sudo snap install hugo --classic
```
### tmux

Because it's nice to leave stuff running, and have multiple screens / panes.

```bash
sudo apt install tmux
```

### TTYD

Self hosts a Terminal over the web. 

( More on this later, it was a complete saga all on it's own )

### HelloSvelte

e.g. do a basic webdev hot-reload  

### Vhost 

Nginx+certbot really shines here.
It's just a matter of writing different server blocks in the config file:

```js
server {
  server_name www.drydave.dev;
  root /var/www/html;
  index index.html;
  location / {
    try_files $uri $uri/ -404;
  }
}

server {
  server_name dev.drydave.dev;
  location / {
    proxy_pass http://127.0.0.1:8080;
    proxy_set_header Host  $host;
    proxy_set_header X-Real-IP $remote_addr
    proxy_set_heaer X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

Then we just tell certbot to configure it for SSL

```bash
sudo certbot --nginx -d www.drydave.dev -d dev.drydave.dev
```
BAM!

certbot inserts the relevant SSL config and redirects http to https.
Now we can browse over there and not keep getting annoyed chrome's warning
that we are being unsafe.  

We can use the 1 public IP and a couple of CNAMES
for our domain and point them a different back-end services:

  - drydave.dev -> this site   
  - dev.drydave.dev -> svelte app with live reload  
  - tty.drydave.dev -> terminal over https  

## Houston

.. we have a problem ..  

WHOA! when i'm typing in hx editor ...
it's too slow and can't keep up with my ESC -> :wq'ing

*LAME!!!*

## More and more and more

So I start thinking "Maybe I need more RAM" ...

> [hal]
I'm sorry Dave, but i'm afraid i can't do that

Looks like we chose poorly. Some VM's can be resized. So i try to rebuild using a VM image that CAN
be resized.

DRAT!

There are not available in my home region. Next step, find a region where they are available. Ok, Montreal looks good!
But you have to switch to a paid account to add a region. OK. So i'll just make sure
that we dont accidentally do payola stuff by adding a billing alert with a threshold of 0.01 dollars.

Whoohoo! Where up an running.

## BILL BILLS BILLS 

The next day i get an email that my billing threshold has been reached.  

>NOOOO!

It turns out Montreal isn't totally free. Disk space cost money.

> 
sooooo disappointing!
I intend to write a strongly worded letter to the AI bot that suggested using Montreal.


Ok, let's try a different region. Boom! It works.

HOWEVER .... my editor still freaks out on me. 

So i ask The Bot ... 

He/she/they/it tells me

> tmux.conf

```bash
set -sg escape-time 5
```

ARE you kidding me?
I just lost 3 days of my life because of a tmux setting?

