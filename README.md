# Plover Ninja

![Ninja Dolores](https://user-images.githubusercontent.com/4440360/175838091-cd6ff154-dd29-4bca-b2de-353db3a4a8ae.png "Dolores Ninja")

## What does Plover Ninja do?

Plover Ninja notes the words that you steno and how long it takes to write these words. Based on this information, it is able to do some neat analysis. The plugin can:

* Determine which words take the longest to write on average
* Determine which words you haven't ever written before

Based on this kind of information, Plover Ninja can make some practice recommendations. In order for its suggestions to be useful, Plover Ninja keeps in mind which words are used most frequently (based on [this data](https://github.com/IlyaSemenov/wikipedia-word-frequency)). With this information in mind, the plugin can suggest:

* Words that are worth practicing, because they are both slow *and* are fairly common
* The most common words that you have never written before

While there are several tools that can help you practice steno, Plover Ninja is unique in that all of its feedback is based on the things you actually write. If you write an email and hit a tricky word, Plover Ninja will see that and be able to point that out later. If you've never used a common word, Plover Ninja will let you know so that you can grow your vocabulary with useful words.

## Setup

Once you have installed Plover Ninja using the [Plover Plugins Manager](https://github.com/openstenoproject/plover/wiki/Plugins), you will need to enable the plugin in Plover.

To do this, first click on the Configure gear icon:

![Plover Configuration Gear](https://user-images.githubusercontent.com/4440360/175838136-1ce6b8aa-93e2-488b-a2f2-cb83ef6282f4.png "Configuration Gear")

.. then, click on the Plugins tab and click to enable the `ninja_extension`.

![Plugins Tab](https://user-images.githubusercontent.com/4440360/175838184-3af2303a-36a1-44ab-a81a-32eb8b476226.png "Plugins Tab")

## Usage

You interact with Plover Ninja by.. writing commands! The general format of each command is:

`Command phrase` followed by three returns. The three returns are a special cue to Plover Ninja that what you just wrote should be interpreted as a command. If Plover Ninja recognizes your command, it will take action!

Here is a list of commands currently supported by Plover Ninja

### I am ready to practice

Entering `I am ready to practice` followed by three returns will generate some suggestions for practice words. Currently this includes two sections:

* A list of common words that you have not written yet, and
* A list of words that take a while to write, on average, and are fairly common

The output from this command will look something like this:

![Practice Words](https://user-images.githubusercontent.com/4440360/175838207-033c6cd0-dc15-49a1-b495-c3504a731d30.png "Practice Words")

### Show stats

Entering `Show stats` followed by three returns will list how many words you have steno-ed each day.

The output from this command will look something like this:

![Shows stats](https://user-images.githubusercontent.com/4440360/175838228-caac6c2e-4614-4e46-a7fa-8a3a9d7fa9d9.png "Show stats")

There are a few variations on this command, which show your daily word count for different lengths of time:

* `Show week` will show you daily stroke counts for the past week, and
* `Show month` will show you daily stroke counts for the past month

## FAQ

Q: When entering a command, does the case matter?

A: Nope! Feel free to use any case

---

Q: Where does Plover Ninja store its data?

A: In a [SQLite](https://www.sqlite.org/index.html) database located at `$USER_HOME/.plover_ninja/ninja.db`

---

Q: What steps does Plover Ninja take to protect my data?

A:

* **All Plover Ninja data remains local.**
* Your `ninja.db` database is created with user-only read, write, and execute permissions.
