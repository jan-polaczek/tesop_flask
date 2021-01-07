Feature: Registration
  Scenario: Successful registration
    Given The user navigates to the registration page
    And The user enters valid username, email and password
    When The user presses the submit button
    Then The user is successfully registered

  Scenario: Failed registration
    Given The user navigates to the registration page
    And The user enters invalid username, email and/or password
    When The user presses the submit button
    Then The user is not registered