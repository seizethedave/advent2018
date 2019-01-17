#include <fstream>
#include <string>
#include <iostream>
#include <sstream>
#include <utility>
#include <map>
#include <forward_list>
#include <stack>
#include <cassert>

/*
A sequence of current heads, which are each just x,y coordinates.

Every transition, note the "door", which becomes a path on a DAG.
And note every "seen" coordinate, which are the vertices in the DAG.
*/

using Point = std::pair<int, int>;

inline void get_increment(const char dir, char* pdx, char* pdy)
{
  switch (dir)
  {
      case 'W':
        *pdx = -1;
        *pdy = 0;
      break;
      case 'E':
        *pdx = 1;
        *pdy = 0;
      break;
      case 'N':
        *pdx = 0;
        *pdy = -1;
      break;
      case 'S':
        *pdx = 0;
        *pdy = 1;
      break;
      default:
        assert(false);
  }
}

struct ExpInfo
{
public:
  std::forward_list<std::forward_list<Point>*>* alternates;
  std::forward_list<Point>* heads;
};

void debug(
  const std::forward_list<Point>* heads,
  const std::forward_list<std::forward_list<Point>*>* alternates)
{
  std::ostringstream heads_str;

  for (auto p : *heads)
  {
    heads_str << "(" << p.first << "," << p.second << ") ";
  }

  std::ostringstream alternates_str;

  for (auto h : *alternates)
  {
    for (auto p : *h)
    {
      alternates_str << "(" << p.first << "," << p.second << ") ";
    }
  }

  std::cout <<
    "heads = " << heads_str.str() <<
    "alts  = " << alternates_str.str() <<
    std::endl
    ;
}

int main ()
{
  // ^E(NNN|)
  // (E|W)(NN|SS)
  // (E|W)N(E(N|W)E)W

  std::stack<ExpInfo*> depth_stack;

  auto heads = new std::forward_list<Point>({std::make_pair(0, 0)});
  auto next_heads = new std::forward_list<Point>;
  auto alternates = new std::forward_list<std::forward_list<Point>*>;

  std::multimap<Point, Point> edges;
  char dx, dy;

  std::fstream input("advent20-1.txt", std::ios::in);
  char ch;

  uint32_t offset = 0;

  while (std::char_traits<char>::not_eof(ch = input.get()))
  {
    ++offset;
    if (ch == '^' || ch == '$')
    { }
    else if (ch == '(')
    {
      auto info = new ExpInfo();
      info->alternates = alternates;
      info->heads = heads;
      depth_stack.push(info);
      alternates = new std::forward_list<std::forward_list<Point>*>;
      // Copy heads from parent scope.
      heads = new std::forward_list<Point>(*info->heads);
    }
    else if (ch == ')')
    {
      alternates->push_front(heads);

      // Pop depth_stack, merge current alternates into previous ones.
      ExpInfo* parent_info = depth_stack.top();
      depth_stack.pop();
      next_heads->clear();

      //debug(heads, alternates);

      for (auto alternate_heads : *alternates)
      {
        for (auto my_head : *alternate_heads)
        {
          next_heads->push_front(my_head);
        }

        //delete alternate_heads;
      }

      delete alternates;
      heads = next_heads;
      next_heads = new std::forward_list<Point>;
      alternates = parent_info->alternates;
      delete parent_info->heads;
      delete parent_info;

      //debug(heads, alternates);
    }
    else if (ch == '|')
    {
      alternates->push_front(heads);
      ExpInfo* exp_info = depth_stack.top();
      heads = new std::forward_list<Point>(*exp_info->heads);
    }
    else if (ch == '\n')
    { }
    else
    {
      get_increment(ch, &dx, &dy);
      next_heads->clear();

      uint32_t ct = 0;

      for (auto point : *heads)
      {
        ct++;
        Point successor = std::make_pair(point.first + dx, point.second + dy);
        std::cout << offset << " " << ct << " (" << ch << ") " << successor.first << " " << successor.second << std::endl;
        // edges.insert({point, successor});
        next_heads->push_front(successor);
      }

      std::swap(heads, next_heads);
    }
  }

  int ct = 0;
  for (auto g : *heads)
    ct++;
  std::cout << "head count = " << ct << std::endl;

  return 0;
}
