import time
import pandas as pd
import numpy as np
import datetime as dt
import click

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ('january', 'february', 'march', 'april', 'may', 'june')

weekdays = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday')


def user_choice(prompt, user_choices=('y', 'n')):
    """Return  valid input from the user given an array of possible answers.
    """

    while True:
        user_choice = input(prompt).lower().strip()
        # finish the program if the input is end
        if user_choice == 'end':
            raise SystemExit
        # triggers if the input has only one name
        elif ',' not in user_choice:
            if user_choice in user_choices:
                break
        # triggers if the input has more than one name
        elif ',' in user_choice:
            user_choice = [i.strip().lower() for i in user_choice.split(',')]
            if list(filter(lambda x: x in user_choices, user_choice)) == user_choice:
                break

        prompt = ("\nSomething is not right. Please mind the formatting and "
                  "be sure to enter a valid option:\n>")

    return user_choice


def get_filters():
    """Ask  a user to specify city(ies) and filters, month(s) and weekday(s).
    Returns:
        (str) city - name of the city(ies) to analyze
        (str) month - name of the month(s) to filter
        (str) day - name of the day(s) of week to filter
    """

    print("\n\nLet's explore some US bikeshare data!\n")

    print("Type end at any time if you would like to exit the program.\n")

    while True:
        city = user_choice("\nFor what city(ies) do you want to filter the bikeshare data. "
                      "New York City, Chicago or Washington?"
                      "\n>", CITY_DATA.keys())
        month = user_choice("\n From January to June, for what month(s) do you "
                       "want to filter the bikeshare data \n>",
                       months)
        day = user_choice("\nFor what weekday(s) do you want do filter bikeshare "
                     "data? \n>", weekdays)

        # confirm the user input
        confirmation = user_choice("\n Please let us know if you are sure to apply "
                              "the following filter(s) to the bikeshare data."
                              "\n\n City(ies): {}\n Month(s): {}\n Weekday(s)"
                              ": {}\n\n [y] Yes\n [n] No\n\n>"
                              .format(city, month, day))
        if confirmation == 'y':
            break
        else:
            print("\nLet's try this again!")
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """Load data for the specified filters of city(ies), month(s) and
       day(s) whenever applicable.
    Args:
        (str) city - name of the city(ies) to analyze
        (str) month - name of the month(s) to filter
        (str) day - name of the day(s) of week to filter
    Returns:
        df - Pandas DataFrame containing filtered data
    """

    print("\nThe program is loading the data for the filters of your choice.")
    start_time = time.time()

    # filtering data according to the selected city 
    if isinstance(city, list):
        df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city),
                       sort=True)
        # reorganize DataFrame columns after a city concat
        try:
            df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time',
                                     'Trip Duration', 'Start Station',
                                     'End Station', 'User Type', 'Gender',
                                     'Birth Year'])
        except:
            pass
    else:
        df = pd.read_csv(CITY_DATA[city])

    # create columns to display statistics
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour

    # filter the data according to month and weekday into two new DataFrames
    if isinstance(month, list):
        df = pd.concat(map(lambda month: df[df['Month'] ==
                           (months.index(month)+1)], month))
    else:
        df = df[df['Month'] == (months.index(month)+1)]

    if isinstance(day, list):
        df = pd.concat(map(lambda day: df[df['Weekday'] ==
                           (day.title())], day))
    else:
        df = df[df['Weekday'] == day.title()]

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)

    return df


def time_stats(df):
    """Display statistics on the most frequent times of travel."""

    print('\nDisplaying the statistics on the most frequent times of '
          'travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['Month'].mode()[0]
    print('For your selections, the month with the most travels is: ' +
          str(months[most_common_month-1]).title() + '.')

    # display the most common day of week
    most_common_day = df['Weekday'].mode()[0]
    print('For your selections, the most common day of the week is: ' +
          str(most_common_day) + '.')

    # display the most common start hour
    most_common_hour = df['Start Hour'].mode()[0]
    print('For your selection, the most common start hour is: ' +
          str(most_common_hour) + '.')

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def station_stats(df):
    """Display statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = str(df['Start Station'].mode()[0])
    print("For your selections, the most common start station is: " +
          most_common_start_station)

    # display most commonly used end station
    most_common_end_station = str(df['End Station'].mode()[0])
    print("For your selections, the most common start end is: " +
          most_common_end_station)

    # display most frequent combination of start station and
    # end station trip
    df['Start-End Combination'] = (df['Start Station'] + ' - ' +
                                   df['End Station'])
    most_common_start_end_combination = str(df['Start-End Combination']
                                            .mode()[0])
    print("For your selections, the most common startand end combination "
          "of stations is: " + most_common_start_end_combination)

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = (str(int(total_travel_time//86400)) +
                         'd ' +
                         str(int((total_travel_time % 86400)//3600)) +
                         'h ' +
                         str(int(((total_travel_time % 86400) % 3600)//60)) +
                         'm ' +
                         str(int(((total_travel_time % 86400) % 3600) % 60)) +
                         's')
    print('For your selections, the total travel time is : ' +
          total_travel_time + '.')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = (str(int(mean_travel_time//60)) + 'm ' +
                        str(int(mean_travel_time % 60)) + 's')
    print("For your selections , the mean travel time is : " +
          mean_travel_time + ".")

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def user_stats(df, city):
    """Display statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_string()
    print("available number of people user types:")
    print(user_types)

    # Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts().to_string()
        print("\n available number of people for each gender:")
        print(gender_counts)
    except KeyError:
        print("oops!!! There is no data of user genders for {}."
              .format(city.title()))

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = str(int(df['Birth Year'].min()))
        print("\nFor your selections, the oldest person to ride"
              " the bike was born in: " + earliest_birth_year)
        most_recent_birth_year = str(int(df['Birth Year'].max()))
        print("For your selections, the youngest person to ride "
              " the bike was born in: " + most_recent_birth_year)
        most_common_birth_year = str(int(df['Birth Year'].mode()[0]))
        print("For your selections, the most common birth year amongst "
              "users is: " + most_common_birth_year)
    except:
        print("Opps!! There is no data of birth year for {}."
              .format(city.title()))

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def raw_data(df):
    """Display 5 line of sorted raw data each time."""

    print("\nYou have a choice of viewing raw data.")

    # this variable holds where the user last stopped
    request = input('Would you like to see five lines of raw data for the city of interest?\n\n [y] Yes\n [n] No\n\n')
    x=0
    y=5
    if request == 'y':
        print(df[x:y])
        request_again = input('Would you like to see five more lines? \n\n [y] Yes\n [n] No\n\n')
        while request_again == 'y':
            x += 5
            y += 5
            print(df[x:y])
            request_again = input('Would you like to see five more lines? \n\n [y] Yes\n [n] No\n\n')
            if request_again == 'n':
                break
def main():
    while True:
        click.clear()
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        raw_data(df)

        restart = user_choice("\nWould you like to restart?\n\n[y]Yes\n[n]No\n\n>")
        if restart.lower() != 'y':
            break

         
if __name__ == "__main__":
    main()