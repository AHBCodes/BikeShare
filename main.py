import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ('january', 'february', 'march', 'april', 'may', 'june')

weekdays = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')


def getting_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    global filtering, city
    month = ''
    day = ''
    print('Hello! Let\'s explore some US bikeshare data!')
    # getting the user choice for city.
    print("Which city would you like to see the data for? \n you can choose either Chicago, New York City, or Washington.\n")
    while True:
        try:
            city_choice = str(input('Enter the City name: ')).lower().strip()
        except KeyboardInterrupt:
            print('You have chosen to stop the program yourself')
            break
        if city_choice in CITY_DATA:
            city = city_choice
            break
        else:
            print('Please re-enter your city of choice and use one of the following (chicago, new york city and washington)')

    print('Would you like to filter the data by month or day or both or NO filter "for no filter write NO" ?')
    while True:
        try:
            filtering = str(input('Enter filter type: ')).lower().strip()
        except KeyboardInterrupt:
            print('You have chosen to stop the program yourself')
        # get user input for month (all, january, february, ... , june)
        if filtering == 'month':
            print("Which month would you like to choose January, February, March, April, May, or June?")
            while True:
                try:
                    m_filter = str(input('Choose a month to filter with: ')).lower().strip()
                except KeyboardInterrupt:
                    print('You have chosen to stop the program yourself')
                    break
                if m_filter in months:
                    month = m_filter
                    day = 'all'
                    break
                else:
                    print('This is not a valid month please choose from (january, february, march, april, may, june')
            break
        # getting user input for day of week
        elif filtering == 'day':
            print("Available days: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday")
            while True:
                try:
                    d_filter = str(input('Choose a day to filter with: ')).lower().strip()
                except KeyboardInterrupt:
                    print('You have chosen to stop the program yourself')
                    break
                if d_filter in weekdays:
                    day = d_filter
                    month = 'all'
                    break
                else:
                    print('This is not a valid day please enter from (Monday, Tuesday, Wednesday, Thursday, Friday, '
                          'Saturday, or Sunday)')
            break
        elif filtering == 'both':
            print("You have chosen to filter the data via both month and day\nplease note that the available months "
                  "are : January, February, March, April, May, or June and the available days are: Monday, Tuesday, "
                  "Wednesday, Thursday, Friday, Saturday, or Sunday\n please choose one of each")
            while True:
                try:
                    m_filter = str(input('Choose a month to filter with: ')).lower().strip()
                    d_filter = str(input('Choose a day to filter with: ')).lower().strip()
                except KeyboardInterrupt:
                    print('You have chosen to stop the program yourself')
                    break
                if m_filter in months and d_filter in weekdays:
                    month = m_filter
                    day = d_filter
                    break
                else:
                    print('You have either entered an invalid month or day, please try again')
            break
        elif filtering == 'no':
            month = 'all'
            day = 'all'
            break
        else:
            print("This is not a valid entry, please enter (month, day or NO)")
    print('-' * 40)
    return city, month, day


def loading_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # loading data file into a dataframe
    dafr = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    dafr['Start Time'] = pd.to_datetime(dafr['Start Time'])

    # extract month and day of week from Start Time to create new columns
    dafr['month'] = dafr['Start Time'].dt.month
    dafr['day'] = dafr['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        dafr = dafr[dafr['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        dafr = dafr[dafr['day'] == day.title()]

    return dafr


def time_stats(dafr):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    com_month = dafr['month'].mode()[0]
    print('Most Common Start Month is: {}'.format(com_month))
    # display the most common day of week
    com_day = dafr['day'].mode()[0]
    print('Most Common Start Day is: {}'.format(com_day))
    # display the most common start hour
    dafr['Start Time'] = pd.to_datetime(dafr['Start Time'])
    dafr['hour'] = dafr['Start Time'].dt.hour
    com_hour = dafr['hour'].mode()[0]
    print('Most Common Start Hour is: {}'.format(com_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(dafr):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    com_s_station = dafr['Start Station'].mode()[0]
    print('Most Popular Start Station is: {}'.format(com_s_station))

    # display most commonly used end station
    com_e_station = dafr['End Station'].mode()[0]
    print('Most Popular End Station is: {}'.format(com_e_station))

    # display most frequent combination of start station and end station trip
    com_combination = dafr.groupby(['Start Station', 'End Station']).size().idxmax()
    print('The most frequent combination of stations is: {} AND {}'.format(com_combination[0], com_combination[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(dafr):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    t_t_d = dafr['Trip Duration'].sum()
    print('The total trip duration is: {}'.format(t_t_d))
    # display mean travel time
    m_t_d = dafr['Trip Duration'].mean()
    print('The average trip duration is: {}'.format(m_t_d))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(dafr):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    u_types = dafr['User Type'].value_counts()
    print('Count of user types is:\n {}'.format(u_types.to_string()))

    # Display counts of gender
    if 'Gender' in dafr:
        gender_count = dafr['Gender'].value_counts()
        print('Counts of genders is:\n {}'.format(gender_count.to_string()))
    else:
        print('The city you have chosen has no gender data!')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in dafr:
        eb = dafr['Birth Year'].min()
        print('The earliest year of birth is: {}'.format(eb))
        rb = dafr['Birth Year'].max()
        print('The most recent year of birth is: {}'.format(rb))
        cb = dafr['Birth Year'].mode()[0]
        print('The most common year of birth is: {}'.format(cb))
    else:
        print('The city you have chosen has no birth year data!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def show_raw_data(dafr):
    """Ask the users if they would like want to see a sample of the raw data. Each time the user answers 'yes,
    ' the script will print 5 rows of the data . """

    samples = 0
    while True:
        raw_choice = input('\nWould you like to see a sample of the raw data? Enter yes or no.\n').lower()
        if raw_choice == 'yes':
            print(dafr[samples: samples + 5])
            samples += 5
        else:
            break


def main():
    while True:
        city, month, day = getting_filters()
        dafr = loading_data(city, month, day)

        time_stats(dafr)
        station_stats(dafr)
        trip_duration_stats(dafr)
        user_stats(dafr)
        show_raw_data(dafr)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
