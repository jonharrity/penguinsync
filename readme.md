# Penguinsync

A cross-platform google drive client.

### Background
Google provides 15gb of free cloud storage per google account. In the world of cloud backup for personal use, that's a lot of free storage -- to provide some context, Dropbox starts at ~9usd per month for 1TB of storage. 1TB is obviously much bigger than Google's free 15gb;
but, for the average user who wants a small & simple backup solution, they can save their money using free cloud providers like Google.

Google has an official client for Google Drive, called Backup and Sync. However, there are a few problems with the application, such as a lack of support for linux and limited control over selecting files to sync. 
There are a few unofficial clients which seek to address the afforementioned problems. Each have their own upsides (support for linux) and downsides (fees, no GUI).

### Penguinsync Mission
'Penguin' in the names comes from the linux mascot, a penguin, as creating a google drive client for linux is the primary goal of this application. 
Other goals include:
* Be free of charge
* Provide a clear display of synced files and an easy + effective way of selecting them
* Automatic syncing -- setup once and don't worry again
* Have a simple and fast UI
* Minimize bandwidth usage by sending data as effiently as possible

### Development Status
Penguinsync is currently under active development. Core features such as managing which files users select to sync and uploading files to Google Drive are finished; UI updates and smoothing out edges are now being worked on. 
