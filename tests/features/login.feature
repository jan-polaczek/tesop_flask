Feature: Login
  Scenario: Successful login
    Given The user navigates to the login page
    And The user enters valid username and password
    When The user presses the submit button
    Then The user is logged in successfully

  Scenario: Failed login
    Given The user navigates to the login page
    And The user enters invalid username and password
    When The user presses the submit button
    Then The user is not logged in