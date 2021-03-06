```
Usage: vcd system extension [OPTIONS] COMMAND [ARGS]...

  Manage Extension Services in vCloud Director.

      Examples
          vcd system extension list
              List available extension services.
  
          vcd system extension register cse cse cse vcdext '/api/cluster, /api/cluster/.*, /api/cluster/.*/.*'
              Register a new extension service named 'cse'.
  
          vcd system extension unregister cse
              Unregister an extension service named 'cse'.
  
          vcd system extension info cse
              Get details of an extension service named 'cse'.
      

Options:
  -h, --help  Show this message and exit.

Commands:
  info        show extension details
  list        list extensions
  register    register new extension
  unregister  unregister extension

```
