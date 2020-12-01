import unittest
import sys
import os
from Corpus import Corpus
from Keywords import Keywords
from unittest.mock import patch, Mock, MagicMock, PropertyMock


class KeywordUnitTests(unittest.TestCase):
    def test_constructor__given_short_hockey_sentence__then_correct_keywords_returned(
        self,
    ):
        # Arrange
        corpus = Corpus(corpus_location="./tests/data/hockey/")
        keywords = Keywords(corpus)
        input = "Ovi scored a big goal!"

        # Act
        results = keywords.get_keywords(input)

        # Assert
        expected = ["goal", "ovi scored"]
        self.assertEqual(results.keywords, expected)

    def test_constructor__given_blog_post__then_correct_keywords_returned(
        self,
    ):
        # Arrange
        corpus = Corpus(corpus_location="./tests/data/hockey/")
        keywords = Keywords(corpus)
        input = """
Kolzig on Samsonov Small biz gift guide ‘Jake Paul needs to fight a hockey player’ Ovi on Sergei’s athletic future
The Washington Capitals have won the Stanley Cup!
BY Peter Hassett 451 Comments
June 7, 2018 11:07 pm
Alex Ovechkin and the 2017-18 Washington Capitals have won the Stanley Cup!
Let me tell you how. It’s a story of a captain and his role-players, of big hits and swallowed whistles, of goofy goals and lost leads, of unexpected heroes and dependable stalwarts. Get familiar with this story; you’ll be talking about it for the rest of your life.
After a scoreless first period in which the score was 0-0, things got buckwild. Jakub Vrana got a breakaway to breakout of his scoring slump, but the Knights struck back promptly with a lucky goal by Nate Schmidt, god dammit. Alex Ovechkin responded by drawing a penalty and scoring on the ensuring power play. David Perron got a greasy one, his first goal of the playoffs, that survived a coach’s challenge. Late in the period, Reilly Smith exploited some great puck movement to give Vegas their first lead of the night.
In the third, with an inhuman effort, Devante Smith-Pelly scored yet another massively clutch goal, kicking the puck to his stick and scoring while falling to restore the tie halfway through the third period. Then, with seven minutes left, Lars Eller bumped a loose puck behind Fleury over the goal line to give the Caps the lead. It held.
Caps beat Knights 4-3!
Caps win the series 4-1! 
Caps win the Cup!
Friends, I didn’t know how this game was going to go, so I wrote coverage of the game like it was any other game. Bullets follow, but first, for the last time of the season, let’s dance.
The Lars Eller line was electric from the first puck drop, dominating possession to a degree where I felt that a goal was inevitable. I didn’t know it’d be the Cup-winning goal. That’s nice. Good for him.
I refuse to talk about the Nate Schmidt goal. I won’t hear it, and I won’t respond to it.
Alex Ovechkin has scored 15 goals in 24 playoff games. That’s the same total that Sidney Crosby had in 2009, when he was 21. Except this year Ovechkin is, and I’m not making this up, 76 years old. To score on an Ovi Shot from the Ovi Spot here, the biggest game of his career, on a PP he personally drew through exceptional personal effort, is perfectly appropriate.
I am not in love with Brooks Orpik‘s defense on the Smith goal. Orpik was immobile on the post, giving grief to Bill Karlsson, and getting a darn good look at the puck as it slid into an empty net. Orpik responded by cold-cocking Karlsson, which should have been penalized, but I think the refs had given up at that point.
Orpik redeemed himself with a blue-line keep-in to make possible for Devante Smith-Pelly yet another improbable clutch goal, his third in three games. Once again, DSP kicked the puck to his stick and scored while falling to the ice. DSP’s unexpected jump to power levels over 9000 will be on one of my favorite stories of these playoffs that my grandkids will be sick of hearing it.
Jakub Vrana had been generating offense roughly on par with Ovechkin these playoffs (12 shots, 5 high-danger chances per hour), but he hasn’t had a fraction of the success. After a 12-game goalless streak, Vrana broke through with a breakaway.
GG, VGK. You’re my second favorite team in the NHL. You’ll be back in a couple decades.
 
Real Life Painting of the night
Here’s where I try to wrap it up, but I’m not able to right now. I’ll need time. For now, lemme say this:
I love y’all. It’s been a privilege to share this with you. Thank you.
You can get the Suck shirt in our store
Crash the net.
Full Coverage of Game Five
Share this story:
Share
Email
 060718, 2018 Playoffs, Vegas Golden Knights, Washington Capitals 2018 Stanley Cup Champions
Russian Machine Never Breaks is not associated with the Washington Capitals; Monumental Sports, the NHL, or its properties. Not even a little bit.
All original content on russianmachineneverbreaks.com is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0)– unless otherwise stated or superseded by another license. You are free to share, copy, and remix this content so long as it is attributed, done for noncommercial purposes, and done so under a license similar to this one. 
"""

        # Act
        results = keywords.get_keywords(input)
        print(str(results))

        # Assert
        expected = [
            "goal",
            "orpik",
            "knights",
            "puck",
            "2018",
        ]
        for keyword in expected:
            self.assertTrue(
                keyword in results.keywords,
                f"Expected to find '{keyword}' in {results.keywords}",
            )

    def test_constructor__given_nhl_wikipedia_page__then_correct_keywords_returned(
        self,
    ):
        # Arrange
        corpus = Corpus(corpus_location="./tests/data/hockey/")
        keywords = Keywords(corpus)
        input = ""
        with open("./tests/data/hockey/nhl_wikipedia.txt", "r") as file:
            input = file.read()

        # Act
        results = keywords.get_keywords(input)
        print(str(results))

        # Assert
        expected = ["hockey league", "stanley cup"]
        for keyword in expected:
            self.assertTrue(
                keyword in results.keywords,
                f"Expected to find '{keyword}' in {results.keywords}",
            )


if __name__ == "__main__":
    unittest.main()