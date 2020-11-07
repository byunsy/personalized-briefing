from datetime import date
import io

import personal_briefing as pb

""" ===========================================================================
                                     MAIN
=========================================================================== """
def main():

    # This is the HTML template for the personal briefing
    template = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Personal Briefing</title>
    <!-- normalize -->
    <link
      rel="stylesheet"
      href="https://necolas.github.io/normalize.css/8.0.1/normalize.css"
    />
    <!-- font awesome -->
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.11.2/css/all.css"
      integrity="sha256-46qynGAkLSFpVbEBog43gvNhfrOj+BmwXdxFgVK/Kvc="
      crossorigin="anonymous"
    />
    <!-- google fonts api -->
    <link
      rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;900&display=swap"
    />
    <link rel="stylesheet" type="text/css" href="briefing.css">
  </head>
  <body>
    <!-- Title -->
    <section class="title_section">
        <h1 class="page_title">Today's Personal Briefing</h1>
        <h2>{date}</h2>
    </section>

    <!-- Weather -->
    <section class="weather_section">
        <h2 class="section_title">{title_1}</h2>
        <p><strong>As of {cur_time}:</strong></p>
        <table class="table_weather">
            <tr>
                <td class="w_head">Temperature</td>
                <td class="w_data">&nbsp{temp_f}°F&nbsp or&nbsp {temp_c}°C</td>
            </tr>
            <tr>
                <td class="w_head">Conditions</td>
                <td class="w_data">&nbsp{condition}</td>
            </tr>
            <tr>
                <td class="w_head">Wind</td>
                <td class="w_data">&nbsp{wind}</td>
            </tr>
            <tr>
                <td class="w_head">Humidity</td>
                <td class="w_data">&nbsp{humid}</td>
            </tr>
        </table>
        <p><strong>Forecast throughout today:</strong></p>
        <ul class="throughout_day">
            <li>Morning: {mng_temp}</li>
            <li>Afternoon: {afn_temp}</li>
            <li>Evening: {evn_temp}</li>
            <li>Overnight: {ovn_temp}</li>
        </ul>
    </section>

    <!-- COVID -->
    <section class="covid_section">
        <h2 class="section_title">{title_2}</h2>
        <table class="table_covid_cases">
            <tr>
                <td><strong>New cases</strong></td>
                <td class="c_data">&nbsp{cases} (on {cases_date})</td>
            </tr>
            <tr>
                <td><strong>Total cases</strong></td>
                <td class="c_data">&nbsp{total_cases}</td>
            </tr>
        </table>

        <p class="c_summary">{covid_summary}</p>
        
        <p><strong>New cases in neighboring states:</strong></p>
        <table class="table_covid_states">
            <tr>
                <td>{state1}</td>
                <td class="c_data">&nbsp{state1_cases}</td>
            </tr>
            <tr>
                <td>{state2}</td>
                <td class="c_data">&nbsp{state2_cases}</td>
            </tr>
            <tr>
                <td>{state3}</td>
                <td class="c_data">&nbsp{state3_cases}</td>
            </tr>
            <tr>
                <td>{state4}</td>
                <td class="c_data">&nbsp{state4_cases}</td>
            </tr>
            <tr>
                <td>{state5}</td>
                <td class="c_data">&nbsp{state5_cases}</td>
            </tr>
            <tr>
                <td>{state6}</td>
                <td class="c_data">&nbsp{state6_cases}</td>
            </tr>
        </table>
    </section>
    
    <!-- U.S. News -->
    <section class="usnews_section">
        <h2 class="section_title">{title_3}</h2>
        <p>From the New York Times:</p>

        <div class="news bar">
            <h3 class="news_title">1. {us_news1_title}</h3>
            <p>{us_news1_story}</p>
            <a href="{us_news1_link}">Read More</a>
        </div>

        <div class="news bar">
            <h3 class="news_title">2. {us_news2_title}</h3>
            <p>{us_news2_story}</p>
            <a href="{us_news2_link}">Read More</a>
        </div>

        <div class="news">
            <h3 class="news_title">3. {us_news3_title}</h3>
            <p>{us_news3_story}</p>
            <a href="{us_news3_link}">Read More</a>
        </div>
    </section>

    <!-- World News -->
    <section class="worldnews_section">
        <h2 class="section_title">{title_4}</h2>
        <p>From BBC World:</p>

        <div class="news bar">
            <h3 class="news_title">1. {wo_news1_title}</h3>
            <p>{wo_news1_story}</p>
            <a href="{wo_news1_link}">Read More</a>
        </div>

        <div class="news bar">
            <h3 class="news_title">2. {wo_news2_title}</h3>
            <p>{wo_news2_story}</p>
            <a href="{wo_news2_link}">Read More</a>
        </div>

        <div class="news">
            <h3 class="news_title">3. {wo_news3_title}</h3>
            <p>{wo_news3_story}</p>
            <a href="{wo_news3_link}">Read More</a>
        </div>
    </section>

  </body>
</html>
    """

    # Today's date
    today = date.today()
    date_str = today.strftime("%B %d, %Y")

    # Attain all necessary web-scraped data
    weather = pb.get_weather()
    covid = pb.get_covid_cases()
    usa = pb.get_us_headlines()
    world = pb.get_world_headlines()

    # =========================================================================
    # Main Titles
    title_1 = "Weather today in Grinnell, Iowa"
    title_2 = "COVID-19 Cases in Iowa"
    title_3 = "U.S. Headline News"
    title_4 = "World Headline News"

    # =========================================================================
    # Weather Data
    (cur_time, temp_f, temp_c, condition, wind, 
    humid, mng_temp, afn_temp, evn_temp, ovn_temp) = weather

    # =========================================================================
    # COVID Data
    cases, cases_date, total_cases, covid_summary, states = covid

    state1       = list(states.keys())[0]
    state1_cases = list(states.values())[0]

    state2       = list(states.keys())[1]
    state2_cases = list(states.values())[1]

    state3       = list(states.keys())[2]
    state3_cases = list(states.values())[2]

    state4       = list(states.keys())[3]
    state4_cases = list(states.values())[3]

    state5       = list(states.keys())[4]
    state5_cases = list(states.values())[4]

    state6       = list(states.keys())[5].replace("-", " ")
    state6_cases = list(states.values())[5]

    # =========================================================================
    # U.S. Headlines
    us_news1_title, us_news1_story, us_news1_link = usa[0]
    us_news2_title, us_news2_story, us_news2_link = usa[1]
    us_news3_title, us_news3_story, us_news3_link = usa[2]
    
    # =========================================================================
    # World Headlines
    wo_news1_title, wo_news1_story, wo_news1_link = world[0]
    wo_news2_title, wo_news2_story, wo_news2_link = world[1]
    wo_news3_title, wo_news3_story, wo_news3_link = world[2]
    
    # =========================================================================
    # Insert all data into the HTML template
    briefing = template.format(date=date_str, 
                               title_1=title_1, cur_time=cur_time, 
                               temp_f=temp_f, temp_c=temp_c, 
                               condition=condition, wind=wind, humid=humid, 
                               mng_temp=mng_temp, afn_temp=afn_temp, 
                               evn_temp=evn_temp, ovn_temp=ovn_temp, 
                               title_2=title_2, cases=cases, 
                               cases_date=cases_date, total_cases=total_cases, 
                               covid_summary=covid_summary, 
                               state1=state1, state1_cases=state1_cases,
                               state2=state2, state2_cases=state2_cases,
                               state3=state3, state3_cases=state3_cases,
                               state4=state4, state4_cases=state4_cases,
                               state5=state5, state5_cases=state5_cases,
                               state6=state6, state6_cases=state6_cases,
                               title_3=title_3, 
                               us_news1_title=us_news1_title,
                               us_news1_story=us_news1_story, 
                               us_news1_link=us_news1_link,
                               us_news2_title=us_news2_title,
                               us_news2_story=us_news2_story, 
                               us_news2_link=us_news2_link,
                               us_news3_title=us_news3_title,
                               us_news3_story=us_news3_story, 
                               us_news3_link=us_news3_link,
                               title_4=title_4, 
                               wo_news1_title=wo_news1_title,
                               wo_news1_story=wo_news1_story, 
                               wo_news1_link=wo_news1_link,
                               wo_news2_title=wo_news2_title,
                               wo_news2_story=wo_news2_story, 
                               wo_news2_link=wo_news2_link,
                               wo_news3_title=wo_news3_title,
                               wo_news3_story=wo_news3_story, 
                               wo_news3_link=wo_news3_link)

    with io.open("./briefing.html", 'w', encoding='utf8') as f:
        f.write(briefing)
    f.close()

if __name__ == "__main__":
    main()