import time  # time is a module  to handle time-related tasks
import pandas as pd
import numpy as np
import calendar  # calendar module handles operations related to the calendar. 

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #  get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago,New York city,Washington?').lower()
        if city not in CITY_DATA:
            print('Kindly choose a correct city name')
        else:
            break

    # get user input for month (all, january, february, ... , june)

    while True:
        month = input('Which month? January, February, March, April, May, June,or type all to see all months:').lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        if month != 'all' and month not in months:
            print('Kindly enter a full valid month name')
        else:
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(
            'Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or type all to see all days:').lower()
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        if day != 'all' and day not in days:
            print('Kindly enter a full valid day name')
        else:
            break

    print('=' * 50)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def show_raw_data(df):
    """
    Raw data is displayed upon request by the user.

    Args:
         df - Pandas DataFrame containing city data filtered by month and day which has been returned from "load_data()" function

    """
    i = 0
    # prompt the user if they want to see 5 lines of raw data
    user_response = input('Would you like to see the first five lines of raw data? yes/no:').lower()
    while True:
        # Stop the program when the user says 'no' or there is no more raw data to display
        if user_response == 'no':
            break
        print(df[i:i + 5])  # Display that data if the answer is 'yes',
        # Continue iterating these prompts and displaying the next 5 lines of raw data at each iteration
        user_response = input('Would you like to see the first five lines of raw data? yes/no:').lower()
        i += 5


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]  # returns month number
    print("What is the most popular month for traveling?\n",
          calendar.month_name[popular_month])  # convert month number to month name
    #  display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("What is the most popular day for traveling?\n", popular_day)

    #  display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("What is the most popular hour of the day to start your travels?\n", popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('=' * 50)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print("\nWhat is the most popular start station?\n", start_station)

    #  display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print("\nWhat is the most popular end station?\n", end_station)

    # display most frequent combination of start station and end station trip
    common_start_end = (df['End Station'] + " - " + df['Start Station']).mode()[0]
    print("\nmost frequent combination of start station and end station trip:\n", common_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('=' * 50)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\ntotal travel time:', total_travel_time, 'seconds')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nmean travel time:', mean_travel_time, 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('=' * 50)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #  Display counts of user types

    print('What is the breakdown of users?\n', df['User Type'].value_counts())
    #  Display counts of gender
    # note: washington data set has no 'gender' column .if statement to avoid run-time error
    if 'Gender' in df:
        print("\nWhat is the breakdown of gender?\n", df['Gender'].value_counts())
    #  Display earliest, most recent, and most common year of birth
    # note: washington data set has no 'Birth Year' column .if statement to avoid run-time error
    if 'Birth Year' in df:
        earliest_year_of_birth = int(df['Birth Year'].min())
        print('\n Earliest year of birth:\n', earliest_year_of_birth)
        recent_year_of_birth = int(df['Birth Year'].max())
        print('\n Most recent year of birth:\n', recent_year_of_birth)
        common_year_of_birth = int(df['Birth Year'].min())
        print('\n Most common year of birth:\n', common_year_of_birth)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('=' * 50)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        show_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()