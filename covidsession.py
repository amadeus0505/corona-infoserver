from covid.john_hopkins import Covid as JohnHopkinsCovid
import datetime
import os
import time


class Covid(JohnHopkinsCovid):
    def __init__(self):
        super().__init__()
        self.country = ""
        self.confirmed = 0
        self.deaths = 0
        self.reco = 0
        self.first = True

    def validate_country(self, country):
        countries_dict = self.list_countries()
        countries = [country["name"].lower() for country in countries_dict]
        if country.lower() not in countries:
            print("Invalid country: " + country)
            print("Valid countries: " + ", ".join(countries))
            return False
        return True

    def get_all_cases_mod(self) -> list:
        data = self.get_all_cases()
        country_infos = []
        for country_info in data:
            country_infos.append(country_info["attributes"])

        return country_infos

    def get_useful_info_by_country(self, country):
        """
        :returns: list: useful information; format [<country>, <confirmed cases>, <deaths>, <recovered>, <datetime.date object,
        latest update>]
        """
        self.country = country
        info = self.get_status_by_country_name(country)
        update_timestamp = int(info["last_update"])
        date = datetime.datetime.fromtimestamp(update_timestamp / 1000)
        useful = [info["country"], info["confirmed"], info["deaths"], info["recovered"], date]
        if self.first:
            self.set_start_ints(useful[1], useful[2], useful[3])
            self.first = False
        return useful

    def set_start_ints(self, confirmed, deaths, reco):
        self.confirmed = confirmed
        self.deaths = deaths
        self.reco = reco

    def get_difference(self, t_confirmed, t_deaths, t_reco):
        """
        :param t_confirmed: temporary confirmed cases
        :param t_deaths: temporary deaths
        :param t_reco: temporary recovered
        :returns:
            list: difference between start value and temporary value; format: [<confirmed>, <deaths>, <recovered>]
        """

        diff_confirmed = t_confirmed - self.confirmed
        diff_deaths = t_deaths - self.deaths
        diff_reco = t_reco - self.reco

        return [diff_confirmed, diff_deaths, diff_reco]

    @staticmethod
    def sign(num: int):
        if num > 0:
            return "+"
        return ""

    def print_info(self, info, write=False):
        country, confirmed, deaths, reco, date = info
        diff_confirmed, diff_deaths, diff_reco = self.get_difference(confirmed, deaths, reco)
        output = f"Country: {country}\nConfirmed cases: {confirmed:,}\nDeaths: {deaths:,}\nRecovered: {reco:,}\nLast " \
                 f"info update: {date} \n\n"
        diff_output = f"Difference since program start:\nConfirmed cases: {self.sign(diff_confirmed)}" \
                      f"{diff_confirmed:,}\nDeaths: {self.sign(diff_deaths)}{diff_deaths:,}\nRecovered: " \
                      f"{self.sign(diff_reco)}{diff_reco:,} "

        if not write:
            os.system("cls")
            print(output + diff_output)
            print("\nLats info fetch: " + str(datetime.datetime.fromtimestamp(round(time.time(), 0))))
        else:
            filepath = fr"info\corona_{country.lower()}.info"
            with open(filepath, "w") as file:
                file.write(output + diff_output + f"\n\nLats info fetch: "
                                                  f"{datetime.datetime.fromtimestamp(round(time.time(), 0))}")

    def get_country_names(self):
        return [country["name"] for country in self.list_countries()]

    def update_screen(self):
        info = self.get_useful_info_by_country(self.country)
        self.print_info(info, write=True)
