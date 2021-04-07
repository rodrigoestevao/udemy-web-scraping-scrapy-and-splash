
# SCRAPED SITES
- [Books To Scrape](http://books.toscrape.com/)
- [Tiny Deal](https://web.archive.org/web/20190225123327/https://www.tinydeal.com/specials.html/)
- [Live Coin](https://web.archive.org/web/20200116052415/https://www.livecoin.net/en/)
- [Glasses Shop](https://www.glassesshop.com/bestsellers/)
- [ImDb](https://www.imdb.com/chart/top/?ref_=nv_mv_250)
- [National Debt](https://worldpopulationreview.com/countries/countries-by-national-debt/)
- [Worldmeter](https://www.worldometers.info/world-population/population-by-country/)

# Splash Scripts

## [DuckDuckGo](https://duckduckgo.com)
````lua
function main(splash, args)
  user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
  --splash:set_user_agent(user_agent)
  --[[
  headers = {["User-Agent"] = user_agent}
  splash:set_custom_headers(headers)
  --]]
  splash:on_request(
    function(request)
      request:set_header("User-Agent", user_agent)
    end
  )  
  assert(splash:go(args.url))
  assert(splash:wait(0.5))

  input_box = assert(splash:select("#search_form_input_homepage"))
  input_box:focus()
  input_box:send_text("my user agent")
  assert(splash:wait(0.5))
  --[[
  btn = assert(splash:select("#search_button_homepage"))
  btn:mouse_click()
  --]]
  input_box:send_keys("<Enter>")
  assert(splash:wait(2))
  splash:set_viewport_full()
  
  return {
    html = splash:html(),
    png = splash:png(),
    har = splash:har(),
  }
end
````

## [Live Coin](https://web.archive.org/web/20200116052415/https://www.livecoin.net/en/)
````lua
function main(splash, args)
  splash.private_mode_enabled = false
  assert(splash:go(args.url))
  assert(splash:wait(1))
  rur_tab = assert(splash:select_all(".filterPanelItem___2z5Gb "))
  rur_tab[5]:mouse_click()
  assert(splash:wait(1))
  splash:set_viewport_full()
  return splash:html()
end
````

