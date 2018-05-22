**TranslateSkill**
===================

Allow to translate phrases into other languages for Mycroft 18.2.6 or higher

Supported languages:
English, Spanish, French, Italian, Portuguese, Dutch, German, Swedish, Hungarian, Polish, Norwegian, Danish, Romanian, Slovak, Catalan, Chinese and Japanese
----------


Manual Installation on Ubuntu with Dev branch
---------------------------------------------

    cd  /opt/mycroft/skills
    git clone https://github.com/jcasoft/translate-skill.jcasoft.git
    cd translate-skill.jcasoft
    bash requirements.sh    (try with sudo if necessary)
    ~/mycroft-core/.venv/bin/pip install -r requirements.txt    (try with sudo if necessary)

    Restart Mycroft

    ./stop-mycroft.sh
    ./start-mycroft.sh debug




Manual Installation on Picroft and Mark1
----------------------------------------

    cd  /opt/mycroft/skills
    sudo su mycroft
    git clone https://github.com/jcasoft/translate-skill.jcasoft.git
    cd translate-skill.jcasoft
    bash requirements.sh
    /opt/venvs/mycroft-core/bin/pip install -r requirements.txt

    Restart Mycroft Skills

    sudo /etc/init.d/mycroft-skills restart



Notes
--------------------

The installation of requirements (bash requirements.sh) take long time.


Features
--------------------

Currently this skill can do the following things (with some variation):

- translate to spanish good night

- translate good morning my dear friends and happy new year to italian
- translate good morning my dear friends and happy new year to spanish
- translate good morning my dear friends and happy new year to french
- translate good morning my dear friends and happy new year to dutch
- translate good morning my dear friends and happy new year to german
- translate good morning my dear friends and happy new year to portuguese
- translate good morning my dear friends and happy new year to polish
- translate good morning my dear friends and happy new year to danish
- translate good morning my dear friends and happy new year to hungarian
- translate good morning my dear friends and happy new year to swedish
- translate good morning my dear friends and happy new year to norwegian
- translate good morning my dear friends and happy new year to catalan
- translate good morning my dear friends and happy new year to romanian
- translate good morning my dear friends and happy new year to slovak
- translate good morning my dear friends and happy new year to chinese
- translate good morning my dear friends and happy new year to japanese

> **Note:**

> - You can toggle language key word with:
> - spanish, italian, french, dutch, german, portuguese, polish, danish, hungarian, swedish, norwegian, catalan (no good voice quaility), romanian, slovak, chinese, japanese



**Enjoy !**
--------
