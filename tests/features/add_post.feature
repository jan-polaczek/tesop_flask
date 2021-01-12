Feature: Add blog post
  Scenario: Add blog post successfully
    Given The user is logged in
    And The user navigates to the new blog post page
    And The user enters valid blog post data
    When The user presses the submit button
    Then A new blog post is created