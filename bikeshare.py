import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York, or Washington?\n').lower()
    while city not in CITY_DATA:
        city = input('Please type out a city (Chicago, New York, or Washington):\n').lower()
    # return city

    # get user input for month (all, january, february, ... , june)
    month = input('Which month? All, January, February, March, April, May or June?\n').lower()
    while month not in months:
        month = input('Please type out the full month name or all:\n').lower()
    month = months.index(month) # Convert string to day

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day? All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday?\n')
    while day not in days:
        day = input('Please type out the full weekday name or all:\n').lower()

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
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    # filter by month if applicable
    if month != 0:  # 0='all'; 1='january'
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day.lower() != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    print('-'*40)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('{:30} {}'.format('Most common month:', months[common_month].title())) # Convert to string

    # display the most common day of week
    popular_weekday = df['day_of_week'].mode()[0]
    print('{:30} {}'.format('Most common day of week:', popular_weekday.title()))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('{:30} {}'.format('Most common start hour:', popular_hour))

    print("\nThis took %.3f seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('{:30} {}'.format('Most common start station:',popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('{:30} {}'.format('Most common end station:', popular_end_station))

    # display most frequent combination of start station and end station trip
    popular_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    counter_popular = df.groupby(['Start Station', 'End Station']).size().max()
    print('{:30} {} {} {} {}'.format(
        'Most popular trip:', 'From', popular_combination[0], 'to', popular_combination[1]))
    print('{:30} {} {}'.format('', counter_popular, 'times'))


    print("\nThis took %.3f seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    sum_travel_time = int(df['Trip Duration'].sum()) # Convert to native Python integer
    sum_str = str(datetime.timedelta(seconds=sum_travel_time)) # Convert to d:h:m:s string
    print('{:30} {}'.format('Total travel time:', sum_str))

    # display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean()) # Round and convert to native Python integer
    mean_str = str(datetime.timedelta(seconds=mean_travel_time)) # Convert to d:h:m:s string
    print('{:30} {}'.format('Mean travel time:', mean_str))

    print("\nThis took %.3f seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts(sort=True, dropna=False)
    print('Count of user types:')
    for index, value in user_type.items():
        print('{:>30}: {:>10}'.format(index, value))


    # Display counts of gender
    if'Gender' in df.columns:
        gender_cat = df['Gender'].value_counts(sort=True, dropna=False)
        print('\nCount of each gender:')
        for index, value in gender_cat.items():
            print('{:>30}: {:>10}'.format(index, value))
    else:
        print('\nGender information not available')


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth = df['Birth Year'].min()
        recent_birth = df['Birth Year'].max()
        common_birth = df['Birth Year'].mode(dropna = True)
        print('')
        print('{:30} {:>11.0f}'.format('Earliest year of birth:', earliest_birth))
        print('{:30} {:>11}'.format('Most recent year of birth:', int(recent_birth)))
        print('{:30} {:>11}'.format('Most common year of birth:', int(common_birth)))
    else:
        print('\nYear of birth information not available')

    print("\nThis took %.3f seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        row = 0
        while True or row <= df.size:
            view_data = input('\nWould you like to view individual trip data? Enter yes or no.\n')
            if view_data.lower() == 'yes':
                print(df.iloc[row:row+5, 1:]) # Print 5 entries of dataframe
                row += 5
            else:
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
