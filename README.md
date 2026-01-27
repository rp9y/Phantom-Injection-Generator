# Phantom-Injection-Generator

Phantom is an educational project, made to teach how injections work.

It generates Discord Injections, that manipulate Discord's application data to be stealers, not make the app work.

## How do these injections work?
They swap Discord's "index.js" file for the javascript inside of the Phantom Generator, and deliver data to your Discord webhook.
This data includes billing, tokens, e-mails, phone numbers and much more.

Anytime a user changes any information on the account, it logs the token and re-sends it to your webhook.

## How does the generator work?
It opens up a window using your terminal, and asks for your Webhook URL.
After you give it the URL, it will take you to a "saving" page, where you are allowed to put any name you want.
When saved, the generator will automatically try to obfuscate and compile the injector, so that you can deliver it.
