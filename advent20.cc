#include <fstream>
#include <string>
#include <iostream>
#include <utility>
#include <set>
#include <map>
#include <forward_list>

/*
A sequence of current heads, which are each just x,y coordinates.

Every transition, note the "door", which becomes a path on a DAG.
And note every "seen" coordinate, which are the vertices in the DAG.
*/

using Point = std::pair<int, int>;

inline void dir_to_increment(const char dir, char* pdx, char* pdy)
{
  if (dir == 'W')
  {
    *pdx = -1;
    *pdy = 0;
  }
  else if (dir == 'E')
  {
    *pdx = 1;
    *pdy = 0;
  }
  else if (dir == 'N')
  {
    *pdx = 0;
    *pdy = -1;
  }
  else if (dir == 'S')
  {
    *pdx = 0;
    *pdy = 1;
  }
}

int main ()
{
  std::fstream input("advent20-1.txt", std::ios::in);
  char ch;
  // ^E(NNN|)

  std::set<Point> seen {std::make_pair(0, 0)};
  std::forward_list<Point> heads {std::make_pair(0, 0)};
  std::forward_list<Point> next_heads;
  std::multimap<Point, Point> edges;
  char dx, dy;

  while (std::char_traits<char>::not_eof(ch = input.get()))
  {
    switch (ch)
    {
      case '^':
      case '$':
        continue;

      case '(':
        break;
      case ')':
        break;
      case '|':
        break;

      default:
        dir_to_increment(ch, &dx, &dy);
        next_heads.clear();

        for (auto point : heads)
        {
          Point successor = std::make_pair(point.first + dx, point.second + dy);
          std::cout << successor.first << " " << successor.second << std::endl;
          seen.insert(successor);
          edges.insert({point, successor});
          next_heads.push_front(successor);
        }

        heads.swap(next_heads);
    }
  }

  return 0;
}
