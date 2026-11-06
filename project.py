# project.py
"""
Execution START point for the Sounding Rocket Simulator.
Instantiates the primary application orchestra controller and starts the campaign.

iwe Sciencekompass.de -> Inspired by the MORABA MAPHEUS Mission - Germany.
www.moraba.de/en
"""

from controllers.game_controller import GameController


def main():
    # Instantiate the primary controller coordinator framework (MVC)
    controller = GameController()

    # Fire up the chronological simulation campaign pipeline (Phases 0 to 5)
    controller.start_campaign()


if __name__ == "__main__":
    main()
