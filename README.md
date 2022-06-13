# Plover Ninja

![Ninja Dolores](/images/dolores-ninja.png "Dolores Ninja")

## What does Plover Ninja do?

Plover Ninja notes the words that you steno and how long it takes to write these words. Based on this information, it is able to do some neat analysis. The plugin can:

* Determine which words take the longest to write on average
* Determine which words you haven't ever written before

Based on this kind of information, Plover Ninja can make some practice recommendations. In order for it's suggestions to be useful, Plover Ninja keeps in mind which words are used most frequently (based on [this data](https://github.com/IlyaSemenov/wikipedia-word-frequency)). With this information in mind, the plugin can suggest:

* Words that are worth practicing, because they are both slow *and* are fairly common
* The most common words that you have never written before

While there are several tools that can help you practice steno, Plover Ninja is unique in that all of its feedback is based on the things you actually write. If you write an email and hit a tricky word, Plover Ninja will see that and be able to point that out later. If you've never used a common word, Plover Ninja will let you know so that you can grow your vocabulary with useful words.

## Setup

Once you have installed Plover Ninja using the [Plover Plugins Manager](https://github.com/openstenoproject/plover/wiki/Plugins), you will need to enable the plugin in Plover.

To do this, first click on the Configure gear icon:

![Plover Configuration Gear](/images/plover_configure_gear.png "Configuration Gear")

.. then, click on the Plugins tab and click to enable the `ninja_extension`.

![Plugins Tab](/images/plover_enable_plugin.png "Plugins Tab")

## Usage

You interact with Plover Ninja by.. writing commands! The general format of each command is:

`Command phrase` followed by three returns. The three returns are a special cue to Plover Ninja that what you just wrote should be interpreted as a command. If Plover Ninja recognizes your command, it will take action!

Here is a list of commands currently supported by Plover Ninja

### I am ready to practice

Entering `I am ready to practice` followed by three returns will generate some suggestions for practice words. Currently this includes two sections:

* A list of common words that you have not written yet, and
* A list of words that take a while to write, on average, and are fairly common

The output from this command will look something like this:

![Practice Words](/images/practice_words.png "Practice Words")
