+++
date = '2025-11-21T12:22:10Z'
draft = false
title = 'From Container With Love'
authors = ['davidkschwob']
showAuthor = true
showAuthorBottom = true
categories = ["Blog","Writing","Dev"]
tags = ["Post","Docker","Podman","Containers"]
showTableOfContents = true
+++


Running hugo commands inside the container ...

<!--more-->

e.g. So that a local hugo binary is not required.


### Find the container

```powershell
> podman container list
CONTAINER ID  IMAGE                             COMMAND               CREATED       STATUS        PORTS                   NAMES
64440b0f5291  docker.io/hugomods/hugo:std-exts  server -D --bind ...  16 hours ago  Up 6 minutes  0.0.0.0:1313->1313/tcp  drydave_hugo_1
```


### Pass command to execute


```powershell
> podman exec drydave_hugo_1 hugo new from-container-with-love.md
WARN  Module "github.com/nunocoracao/blowfish/v2" is not compatible with this Hugo version: 0.141.0/0.152.2 extended; run "hugo mod graph" for more information.
Content "/src/content/from-container-with-love.md" created
```


### Voila!

```powershell
> ls -l .\content\
-----  256 18 Nov 13:20 about.md
-----  874 21 Nov 07:25 from-container-with-love.md
-----  179 18 Nov 13:17 help.md
d----    - 21 Nov 07:15 posts
----- 6.2k 18 Nov 14:23 resume.md
```
