# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edu.iot.portfolio -t test_experiment.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edu.iot.portfolio.testing.EDU_IOT_PORTFOLIO_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_experiment.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Experiment
  Given a logged-in site administrator
    and an add experiment form
   When I type 'My Experiment' into the title field
    and I submit the form
   Then a experiment with the title 'My Experiment' has been created

Scenario: As a site administrator I can view a Experiment
  Given a logged-in site administrator
    and a experiment 'My Experiment'
   When I go to the experiment view
   Then I can see the experiment title 'My Experiment'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add experiment form
  Go To  ${PLONE_URL}/++add++Experiment

a experiment 'My Experiment'
  Create content  type=Experiment  id=my-experiment  title=My Experiment


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the experiment view
  Go To  ${PLONE_URL}/my-experiment
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a experiment with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the experiment title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
