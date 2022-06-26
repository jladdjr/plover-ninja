# Plover Ninja

![Ninja Dolores](https://github.com/jladdjr/plover-ninja/raw/main/images/dolores-ninja.png "Dolores Ninja")

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

![Plover Configuration Gear](https://github.com/jladdjr/plover-ninja/raw/main/images/plover_configure_gear.png "Configuration Gear")

.. then, click on the Plugins tab and click to enable the `ninja_extension`.

![Plugins Tab](https://github.com/jladdjr/plover-ninja/raw/main/images/plover_enable_plugin.png "Plugins Tab")

## Usage

You interact with Plover Ninja by.. writing commands! The general format of each command is:

`Command phrase` followed by three returns. The three returns are a special cue to Plover Ninja that what you just wrote should be interpreted as a command. If Plover Ninja recognizes your command, it will take action!

Here is a list of commands currently supported by Plover Ninja

### I am ready to practice

Entering `I am ready to practice` followed by three returns will generate some suggestions for practice words. Currently this includes two sections:

* A list of common words that you have not written yet, and
* A list of words that take a while to write, on average, and are fairly common

The output from this command will look something like this:

![Practice Words](https://github.com/jladdjr/plover-ninja/raw/main/images/practice_words.png "Practice Words")

### Show stats

Entering `Show stats` followed by three returns will list how many words you have steno-ed each day.

The output from this command will look something like this:

![Shows stats](https://github.com/jladdjr/plover-ninja/raw/main/images/show_stats.png "Show stats")

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

## Known limitations

* When entering a command, each word in the command must be entered using a single stroke.
