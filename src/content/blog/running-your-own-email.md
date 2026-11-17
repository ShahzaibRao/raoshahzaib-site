---
title: "Running your own email service: what three years taught me"
description: "Three years of operating a permanent email service on Cloudflare: why it is receive-only, why the addresses never expire, and what the real work turns out to be."
slug: "running-your-own-email"
---

By Rao Shahzaib · DevOps

I have paid for an email service for three years that most people never see. It is a permanent email service, not a throwaway one: one account creates up to 100 email addresses on my own domain, and none of them expire. The idea is simple. Most of us hand the same address to every website we sign up for, and then wonder why the spam never stops. A different address for every site means you always know which site shared it, and you can stop using that address without changing your real email anywhere else.

The first decision I made was receive-only. The service receives mail. It does not send it. That sounds like a limitation, and it is, but it is deliberate. Sending email is a different job from receiving it. A sending service has to fight spam filters, manage reputation, and deal with abuse, and one bad actor can get the whole domain blocked for everyone. Receiving is a smaller, cleaner problem: accept the message, store it, show it to the right account. Keeping the scope small is what has let one person operate the service for three years without it becoming a second job.

The whole thing runs on Cloudflare. Workers for the API, Pages for the frontend, D1 for the database. There is no server to patch and no database to babysit. That matters more than it sounds, because the service has to be up when people check their mail, and a one-person operation cannot afford a 3 a.m. pager for a server it owns. The trade is that the service lives and dies by the platform's rules — rate limits, request sizes, and the occasional breaking change — and I have had to learn those rules the way I would learn any vendor.

I run two of these services, webmail on my own domain and a second one on another domain, on separate Cloudflare accounts. The admin console shows 9,513 mailboxes on the webmail side. That number is why the boring parts matter more than the code.

The hard part was never the code. It is everything around it: people who forget their credentials, addresses that need to be recovered, signups that need to be real humans and not bots. I use Turnstile on registration to keep the bots out, and I keep the login and the admin console as separate things, because mixing them is how accounts get compromised. Support is the real work of running a service, and it never shows up in the architecture diagram.

If I started again, I would change two things. First, I would write the policy pages on day one — what the service is, what it is not, and what happens to an account — instead of adding them three years later when a reviewer asks for them. Second, I would decide the limits earlier and say them plainly: 100 addresses, receive-only, permanent while the account is active. Clear limits are a feature. They tell people exactly what they are getting, and they protect the service from being used as something it was never meant to be.
